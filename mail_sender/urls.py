from django.urls import path

from mail_sender.apps import MailSenderConfig
from mail_sender.views import IndexView, ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, \
    ClientDeleteView, MailingSettingsListView, MailingSettingsDetailView, MailingSettingsCreateView, \
    MailingSettingsUpdateView, MailingSettingsDeleteView, PersonalAreaView, MailingMessageCreateView, \
    MailingMessageListView, MailingMessageUpdateView, MailingMessageDeleteView, MailingMessageDetailView, \
    MailingLogListView

app_name = MailSenderConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('personal_area/', PersonalAreaView.as_view(), name='personal_area'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('client_detail/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('client_update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('message_create/', MailingMessageCreateView.as_view(), name='create_message'),
    path('message_list/', MailingMessageListView.as_view(), name='list_messages'),
    path('message_edit/<int:pk>', MailingMessageUpdateView.as_view(), name='update_message'),
    path('message_detail/<int:pk>', MailingMessageDetailView.as_view(), name='detail_message'),
    path('message_delete/<int:pk>', MailingMessageDeleteView.as_view(), name='delete_message'),
    path('mails_list/', MailingSettingsListView.as_view(), name='mails_list'),
    path('mails_detail/<int:pk>', MailingSettingsDetailView.as_view(), name='mails_detail'),
    path('mails_create/', MailingSettingsCreateView.as_view(), name='mails_create'),
    path('mails_edit/<int:pk>', MailingSettingsUpdateView.as_view(), name='mails_edit'),
    path('mails_delete/<int:pk>', MailingSettingsDeleteView.as_view(), name='mails_delete'),
    path('logs/', MailingLogListView.as_view(), name='logs'),
]
