from mailjet_rest import Client
import os


class SendEmail:
    def __init__(self):
        self.api_key = os.environ.get("API_KEY")
        self.api_secret = os.environ.get("API_SECRET")

    def send_email(self, name, email, message):
        mailjet = Client(auth=(self.api_key, self.api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "testudemycarlo@gmail.com",
                        "Name": "Portfolio Message"
                    },
                    "To": [
                        {
                            "Email": "carlomonroy1997@gmail.com",
                            "Name": "Carlo"
                        }
                    ],
                    "Subject": "Your email flight plan!",
                    "TextPart": f"Te intentaron contactar de tu portafolio\n Nombre : {name}!\n Email: {email}\n Message: {message}",
                    "HTMLPart": ''
                }
            ]
        }
        result = mailjet.send.create(data=data)

