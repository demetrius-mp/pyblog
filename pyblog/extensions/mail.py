from flask import Flask
from flask_mailman import Mail, EmailMessage

mail = Mail()


def init_app(app: Flask):
    mail.init_app(app)


def send_mail(subject: str, body: str, to: str):
    msg = EmailMessage(subject, body, to=(to,))
    msg.content_subtype = "html"
    msg.send()
