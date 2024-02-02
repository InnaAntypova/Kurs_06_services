import datetime
import logging
import smtplib

from mail_sender.services import send_mass_mail
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from mail_sender.models import MailingSettings, MailingLog

logger = logging.getLogger(__name__)


def get_task(task, time_now):
    """ Функция обрабатывает рассылку. """
    if task.stop_time.timestamp() > time_now.timestamp() >= task.start_time.timestamp() \
            and task.status == task.SendStatus.CREATED:
        task.status = task.SendStatus.LAUNCHED
        task.save()
        emails_list = get_client(task)
        print(emails_list)
        task.status = task.SendStatus.COMPLETED
        task.save()


def get_client(task):
    """ Функция собирает адреса и отправляет письма. """
    emails_list = []
    for client in task.client.all():
        emails_list.append(client.email)
    print(emails_list)
    send_mass_mail(
        task.message.title,
        task.message.body,
        emails_list
    )
    return emails_list


def my_job():
    """ Ежедневная рассылка."""
    time_now = datetime.datetime.now()
    mailing_tasks = MailingSettings.objects.all()

    for task in mailing_tasks:
        print(task)
        if task.is_active:
            try:
                if task.periodicity == task.Periodicity.DAILY:
                    get_task(task, time_now)

                if task.periodicity == task.Periodicity.WEEKLY:
                    get_task(task, time_now)

                if task.periodicity == task.Periodicity.MONTHLY:
                    get_task(task, time_now)

                log = MailingLog.objects.create(mailing_name=task, last_try=time_now, status=MailingLog.LogStatus.OK,
                                                response='Successful')
                log.save()
            except smtplib.SMTPException:
                log = MailingLog.objects.create(mailing_name=task, last_try=time_now, status=MailingLog.LogStatus.FAILED,
                                                response='Error')
                log.save()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """ Функция удалит из базы записи выполнения заданий старше max_age (7 дней) """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/25"),  # интервал
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлено задание: 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлено еженедельное задание: 'delete_old_job_executions'.")

        try:
            logger.info(" Запуск планировщика...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Остановка планировщика...")
            scheduler.shutdown()
            logger.info("Планировщик остановлен успешно!")
