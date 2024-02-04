from django.db import models
from django.db.models import CASCADE

from config import settings

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    """ Модель для сущности Клиент"""

    email = models.EmailField(verbose_name='Email')
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    owners = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.email} ({self.full_name})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class MailingMessage(models.Model):
    """ Модель для сущности Сообщений для рассылки"""

    title = models.CharField(max_length=100, verbose_name='Тема сообщения')
    body = models.TextField(verbose_name='Текст сообщения')
    owners = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.title} - {self.body}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingSettings(models.Model):
    """ Модель для сущности Рассылка"""

    class Periodicity(models.TextChoices):
        DAILY = 'Ежедневно', 'Daily'
        WEEKLY = 'Еженедельно', 'Weekly'
        MONTHLY = 'Ежемесячно', 'Monthly'

    class SendStatus(models.TextChoices):
        COMPLETED = 'Выполнена', 'Completed'
        CREATED = 'Создана', 'Created'
        LAUNCHED = 'В работе', 'Launched'

    name = models.CharField(max_length=100, verbose_name='Название рассылки')
    client = models.ManyToManyField(Client, related_name='clients', verbose_name='Клиент')
    start_time = models.DateTimeField(verbose_name='Начальное время рассылки')
    stop_time = models.DateTimeField(verbose_name='Конечное время рассылки')
    periodicity = models.CharField(choices=Periodicity.choices, default=Periodicity.DAILY,
                                   verbose_name='Периодичность')
    status = models.CharField(choices=SendStatus.choices, default=SendStatus.CREATED,
                              verbose_name='Статус')
    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE, verbose_name='Сообщение для рассылки')
    owners = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Состояние активности')

    def __str__(self):
        return f'{self.name} / {self.status} ({self.start_time} - {self.stop_time}, {self.periodicity}) ({self.client})'

    class Meta:
        permissions = [
            ('set_active',
             'может менять состояние активности')
        ]

        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLog(models.Model):
    """ Модель для сущности Логов рассылки """

    class LogStatus(models.TextChoices):
        OK = 'Успешно', 'Successfully'
        FAILED = 'Неудачно', 'Failed'
        UNKNOWN = 'Неизвестно', 'Unknown'

    mailing_name = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Название рассылки')
    last_try = models.DateTimeField(verbose_name='Дата и время попытки')
    status = models.CharField(choices=LogStatus.choices, default=LogStatus.UNKNOWN, verbose_name='Статус попытки')
    response = models.CharField(max_length=50, verbose_name='Ответ почтового сервера', **NULLABLE)
    owners = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.mailing_name} ({self.last_try}/{self.status})'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
