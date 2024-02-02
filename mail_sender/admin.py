from django.contrib import admin

from mail_sender.models import Client, MailingSettings, MailingMessage, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'full_name', 'comment', 'owners')


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'start_time', 'stop_time', 'periodicity', 'message', 'status', 'owners')
    list_filter = ('periodicity', 'status')


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'body', 'owners')


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mailing_name', 'last_try', 'status', 'response')
