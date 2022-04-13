from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap

from forms import ContactForm, LoginForm, CreatePostForm
from send_email import EmailManager
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from functools import wraps
from flask_ckeditor import CKEditor

from werkzeug.security import generate_password_hash, check_password_hash
import os




app = Flask(__name__)
app.config["SECRET_KEY"] = "randomstring"
Bootstrap(app)

## Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


# ckeditor to create new posts
ckeditor = CKEditor(app)

## CONNECT TO DB
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

## In here we are creating our database tables
##CONFIGURE TABLES


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    name = db.Column(db.String(1000))
    #This will act like a list of BlogSpot objects attached to eaech user
    #The "authro refers to the author property in the BlogSpot Class
    posts = relationship("BlogPost", back_populates="author")



class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)

    #Create foreign key, the users.id refers to the tablename of User
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Create reference to the User object, the "posts" refers to the posts property in the User class.
    author = relationship("User", back_populates="posts")

    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

# Define user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#Creatim admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorate_function(*args, **kwargs):
        #If id is not 1 then return abort with 403 error
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)
        #Otherwise continue with the route
        return f(*args, **kwargs)
    return decorate_function

@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        password = form.password.data
        if user == None:
            return redirect(url_for('index'))
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('make_post'))
    return render_template("login.html", form=form)

#Creatim admin-only decorator

@app.route('/make-post', methods=['GET','POST'])
@login_required
@admin_only
def make_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_blog = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=date.today().strftime("%B %d, %Y"),
            author=current_user,
            body=form.body.data,
            img_url=form.img_url.data

        )
        db.session.add(new_blog)
        db.session.commit()
    return render_template('make_post.html', form=form)

@app.route('/delete/<int:post_id>')
@login_required
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('index'))




@app.route('/', methods=["POST","GET"])
def index():
    form = ContactForm()
    # here we check if user typed something in contact and if he did we send it with smtp
    if form.validate_on_submit():
        name = form.name.data
        email = form.name.data
        message = form.message.data
        send_email = EmailManager(
            email=email,
            name=name,
            message=message
        )
        send_email.send_email()
        flash("Your message has been sent")
        return redirect(url_for("index"))


    return render_template("index.html", form=form)

@app.route('/posts')
def posts():
    posts = BlogPost.query.all()
    return render_template("posts.html", all_posts=posts)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>')
def show_post(post_id):
    print(post_id)
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post)

@app.route('/register')
def register():
    email = "carlomonroy1997@gmail.com"
    password = generate_password_hash(password='kali1997', method = 'pbkdf2:sha256',
                                      salt_length=8)
    name = 'Carlo Monroy'
    new_user = User(
        email = email,
        password=password,
        name=name
    )
    db.session.add(new_user)
    db.session.commit()



if __name__ == "__main__":
    app.run(debug=True)