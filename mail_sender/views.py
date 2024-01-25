from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView

from mail_sender.models import Client, MailingSettings


class IndexView(TemplateView):
    template_name = 'mail_sender/index.html'


class ClientListView(ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client

    fields = ('email', 'full_name', 'comment')

    def get_success_url(self):
        return reverse('mail_sender:client_list')


class ClientUpdateView(UpdateView):
    model = Client

    fields = ('email', 'full_name', 'comment')

    def get_success_url(self):
        return reverse('mail_sender:client_list')


class ClientDetailView(DetailView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mail_sender:client_list')


class MailingSettingsListView(ListView):
    model = MailingSettings


class MailingSettingsDetailView(DetailView):
    model = MailingSettings


class MailingSettingsCreateView(CreateView):
    model = MailingSettings

    fields = ('email', 'start_time', 'stop_time', 'periodicity', 'status')

    def get_success_url(self):
        return reverse('mail_sender:mails_list')


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings

    fields = ('email', 'start_time', 'stop_time', 'periodicity', 'status')

    def get_success_url(self):
        return reverse('mail_sender:mails_list')


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mail_sender:mails_list')


class PersonalAreaView(TemplateView):
    template_name = 'mail_sender/personal_area.html'
