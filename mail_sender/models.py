from django.db import models
from django.db.models import CASCADE

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    """ Модель для сущности Клиент"""

    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.email} ({self.full_name})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class MailingSettings(models.Model):
    """ Модель для сущности Рассылка"""

    class Periodicity(models.TextChoices):
        DAILY = 'DL', 'Daily'
        WEEKLY = 'WK', 'Weekly'
        MONTHLY = 'ML', 'Monthly'

    class SendStatus(models.TextChoices):
        COMPLETED = 'CMP', 'Completed'
        CREATED = 'CRT', 'Created'
        LAUNCHED = 'LNC', 'Launched'

    email = models.ForeignKey(Client, on_delete=CASCADE, verbose_name='Email')
    start_time = models.DateTimeField(verbose_name='Начальное время рассылки')
    stop_time = models.DateTimeField(verbose_name='Конечное время рассылки')
    periodicity = models.CharField(max_length=2, choices=Periodicity.choices, default=Periodicity.DAILY,
                                   verbose_name='Периодичность')
    status = models.CharField(max_length=3, choices=SendStatus.choices, default=SendStatus.CREATED,
                              verbose_name='Статус')

    def __str__(self):
        return f'{self.email} / {self.status} ({self.start_time} - {self.stop_time}, {self.periodicity})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingMessage(models.Model):
    """ Модель для сущности Сообщений для рассылки"""

    email = models.ForeignKey(Client, on_delete=CASCADE, verbose_name='Email')
    title = models.CharField(max_length=100, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return f'{self.email} - {self.title}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingLog(models.Model):
    """ Модель для сущности Логов рассылки """

    email = models.ForeignKey(Client, on_delete=CASCADE, verbose_name='Email')
    last_try = models.DateTimeField(verbose_name='Дата и время попытки')
    status = models.CharField(max_length=100, verbose_name='Ответ сервера', **NULLABLE)

    def __str__(self):
        return f'{self.email} ({self.last_try}/{self.status})'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'






