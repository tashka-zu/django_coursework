from django.core.mail import send_mail
from django.conf import settings
from .models import MailingAttempt

def send_mailing(mailing):
    recipients = mailing.clients.all()
    for recipient in recipients:
        send_mail(
            mailing.message.title,
            mailing.message.body,
            settings.DEFAULT_FROM_EMAIL,
            [recipient.email],
            fail_silently=False,
        )
