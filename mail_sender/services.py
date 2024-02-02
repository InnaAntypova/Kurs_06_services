from django.core.mail import send_mail

from config import settings


def send_mass_mail(subject: str, message: str, clients_emails_list):
    """ Функция для массовой рассылки писем. """
    mail_subject = subject
    mail_message = message
    send_mail(
        mail_subject,
        mail_message,
        settings.EMAIL_HOST_USER,
        clients_emails_list
    )


