from django.core.mail import send_mail
from django.urls import reverse

from config import settings


def send_verify_email(user):
    """ Функция для отправки письма верификации пользователя"""
    domain = 'http://127.0.0.1:8000/'
    send_mail(
        f'Подтверждение регистрации в сервисе рассылок.',
        f"""Для подтверждения Вашего аккаунта перейдите по ссылке ниже \n
            {domain}{reverse('users:confirm_registration', kwargs={'uuid': user.field_uuid})}""",
        settings.EMAIL_HOST_USER,
        [user.email]
    )
