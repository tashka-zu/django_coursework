from allauth.account.adapter import DefaultAccountAdapter
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, user, emailconfirmation, signup):
        subject = "Подтверждение адреса электронной почты"
        context = {
            "user": user,
            "emailconfirmation": emailconfirmation,
            "signup": signup,
        }
        html_message = render_to_string('mailing/email_confirmation.html', context)
        message = EmailMultiAlternatives(
            subject=subject,
            body='',
            from_email=self.get_from_email(),
            to=[emailconfirmation.email_address.email]
        )
        message.attach_alternative(html_message, "text/html")
        message.send()
