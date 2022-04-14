from mailjet_rest import Client
import os


class SendEmail:
    def __init__(self):
        self.api_key = "82cc6b59d6b7586f051b94fe145962c5"
        self.api_secret = "ace6b72730a0955817ad241451326fa6"

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

