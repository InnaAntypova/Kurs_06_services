from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        """ Создание администратора """
        superuser = User.objects.create(
            email='admin@dominion.ru',
            is_superuser=True,
            is_active=True,
            is_staff=True
        )
        superuser.set_password('aaa12345')
        superuser.save()
