import os
from threading import Thread

from flask import Flask, current_app
from flask_mailman import Mail, EmailMessage

mail = Mail()


def init_app(app: Flask):
    env_vars = ('MAIL_PASSWORD', 'MAIL_PORT', 'MAIL_SERVER', 'MAIL_USERNAME',
                'MAIL_USE_SSL')

    for env_var in env_vars:
        if env_var not in app.config:
            app.config[env_var] = os.environ.get(env_var)

    mail.init_app(app)


def send_async_email(app: Flask, msg: EmailMessage):
    with app.app_context():
        msg.send()


def send_email(subject: str, body: str, to: str):
    msg = EmailMessage(subject, body, to=(to,))
    # noinspection PyUnresolvedReferences,PyProtectedMember
    app = current_app._get_current_object()
    Thread(target=send_async_email, args=(app, msg)).start()
