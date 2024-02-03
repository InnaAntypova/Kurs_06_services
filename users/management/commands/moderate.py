from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        moderator_group, created = Group.objects.get_or_create(name='Moderator')
        if created:
            permissions = Permission.objects.filter(
                codename__in=['view_mailingsettings', 'change_mailingsettings', 'set_active', 'view_user', 'set_active']
            )

            moderator_group.permissions.set(permissions)

        blog_manager_group, created = Group.objects.get_or_create(name='BlogManager')
        if created:
            permissions = Permission.objects.filter(
                codename__in=['add_article', 'view_article', 'change_article', 'delete_article']
            )
            blog_manager_group.permissions.set(permissions)
