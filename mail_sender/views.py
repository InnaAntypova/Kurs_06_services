from urllib import request

from django.forms import inlineformset_factory

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView

from mail_sender.forms import MailingMessageForm, MailingSettingsForm, ClientForm
from mail_sender.models import Client, MailingSettings, MailingMessage


class IndexView(TemplateView):
    template_name = 'mail_sender/index.html'


class ClientListView(ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mail_sender:client_list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mail_sender:client_list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.save()
        return super().form_valid(form)


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
    form_class = MailingSettingsForm

    def get_success_url(self):
        return reverse('mail_sender:mails_list')

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     MessageFormset = inlineformset_factory(Client, MailingMessage, form=MailingMessageForm)
    #     if self.request.method == 'POST':
    #         context_data['formset'] = MessageFormset(self.request.POST, instance=self.object, extra=1, max_num=1)
    #     else:
    #         context_data['formset'] = MessageFormset(instance=self.object)
    #     return context_data
    #
    # def form_valid(self, form):
    #     formset = self.get_context_data()['formset']
    #     self.object = form.save()
    #     if formset.is_valid():
    #         formset.instance = self.object
    #         formset.save()
    #     return super().form_valid(form)


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm

    def get_success_url(self):
        return reverse('mail_sender:mails_list')


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mail_sender:mails_list')


class PersonalAreaView(TemplateView):
    template_name = 'mail_sender/personal_area.html'


class MailingMessageCreateView(CreateView):
    model = MailingMessage
    form_class = MailingMessageForm

    def get_success_url(self):
        return reverse('mail_sender:mails_create')
