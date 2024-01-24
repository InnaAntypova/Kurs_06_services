from django.urls import path

from mail_sender.apps import MailSenderConfig
from mail_sender.views import IndexView, ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, \
    ClientDeleteView, MailingSettingsListView, MailingSettingsDetailView, MailingSettingsCreateView, \
    MailingSettingsUpdateView, MailingSettingsDeleteView

app_name = MailSenderConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('client_detail/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('client_update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('mails_list/', MailingSettingsListView.as_view(), name='mails_list'),
    path('mails_detail/<int:pk>', MailingSettingsDetailView.as_view(), name='mails_detail'),
    path('mails_create/', MailingSettingsCreateView.as_view(), name='mails_create'),
    path('mails_edit/<int:pk>', MailingSettingsUpdateView.as_view(), name='mails_edit'),
    path('mails_delete/<int:pk>', MailingSettingsDeleteView.as_view(), name='mails_delete'),
]
