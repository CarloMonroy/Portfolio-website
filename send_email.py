import smtplib
import os

email= os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")

class EmailManager():
    def __init__(self, email, name, message):
        self.email = email
        self.name = name
        self.message = message

    def send_email(self):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(
                from_addr=email,
                to_addrs="carlomonroy1997@gmail.com",
                msg = f"Subject:New message from your portfolio\n\nname={self.name}\nemail={self.email}\nmessage={self.message}"
            )

