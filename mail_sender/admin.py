from django.contrib import admin

from mail_sender.models import Client, MailingSettings, MailingMessage, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'full_name', 'comment')


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'start_time', 'stop_time', 'periodicity', 'status')
    list_filter = ('periodicity', 'status')


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'title', 'body')


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'last_try', 'status')
