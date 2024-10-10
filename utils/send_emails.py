from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from chat_platform import settings


def send_email_to(template_name,to,subject,contex):

        html_message1 = render_to_string(template_name, contex)
        plain_message = strip_tags(html_message1)
        from_email = settings.EMAIL_HOST_USER
        return send_mail(subject, plain_message, from_email, [to], html_message=html_message1)

