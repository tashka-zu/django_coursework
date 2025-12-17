from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

from .models import MailingAttempt

def send_mailing(mailing):
    """
    Отправляет сообщения всем клиентам из рассылки.
    """
    for client in mailing.clients.all():
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                mailing=mailing,
                status='Успешно',
                server_response='Сообщение отправлено'
            )
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status='Не успешно',
                server_response=str(e)
            )


def send_confirmation_email(user):
    subject = "Подтверждение регистрации"
    context = {'user': user}
    html_message = render_to_string('mailing/email_confirmation.html', context)
    message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    message.attach_alternative(html_message, "text/html")
    message.send()
