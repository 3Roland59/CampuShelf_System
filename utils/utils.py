from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from random import sample
from string import ascii_uppercase, ascii_lowercase, digits
import requests


def generate_code(max=4, reset_password=False):
    codes = digits + ascii_lowercase + ascii_uppercase
    if reset_password:
        codes = digits
    code = sample(population=codes, k=max)
    return "".join(code)


class SendEmail:
    def __init__(self, user_email, template: str, subject: str, context: dict) -> None:
        self.user_email = user_email
        self.template = template
        self.context = context
        self.render = render_to_string
        email_body = self.render(template, self.context)
        self.email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=[user_email],
        )

    def send_email(self):
        self.email.content_subtype = "html"
        self.email.send()


def send_sms_message(phone, template, context):
    msg = render_to_string(template, context)
    endpoint = "https://apps.mnotify.net/smsapi/"
    params = {
        "key": settings.SMS_API_KEY,
        "to": phone,
        "msg": msg,
        "sender_id": settings.SENDER_ID,
    }
    requests.post(url=endpoint, params=params)
