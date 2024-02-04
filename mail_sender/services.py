from django.core.cache import cache
from django.core.mail import send_mail

from config import settings
from mail_sender.models import Client, MailingSettings


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


def get_client_cache(user):
    """ Сервисная функция для кеширования клиентов пользователя """
    key = 'client_list'
    client_list = cache.get(key)
    if client_list is None:
        client_list = Client.objects.filter(owners=user)
        cache.set(key, client_list)
    return client_list


def get_mailingsettings_cache(user):
    """ Сервисная функция для кеширования списка рассылок пользователя """
    key = 'mailingsettings_list'
    mailingsettings_list = cache.get(key)
    if mailingsettings_list is None:
        if user.groups.filter(name='Moderator').exists() or user.is_superuser:
            mailingsettings_list = MailingSettings.objects.all()
            cache.set(key, mailingsettings_list)
        else:
            mailingsettings_list = MailingSettings.objects.filter(owners=user)
            cache.set(key, mailingsettings_list)
    return mailingsettings_list
