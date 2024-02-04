from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView

from blog.models import Article
from mail_sender.forms import MailingMessageForm, MailingSettingsForm, ClientForm, ModeratorMailingSettingsForm
from mail_sender.models import Client, MailingSettings, MailingMessage, MailingLog

# class FormValidMixin(FormMixin):
#     def form_valid(self, form):
#         if form.is_valid():
#             self.object = form.save()
#             self.object.owners = self.request.user  # владелец
#             self.object.save()
#         return super().form_valid(form)
#
#     def form_valid_update(self, form):
#         if self.object.owners == self.request.user:
#             self.object.owners = self.request.user
#             self.object.save()
#         if form.is_valid():
#             self.object = form.save()
#             self.object.save()
#         return super().form_valid(form)


class IndexView(TemplateView):
    """ Контроллер для главной страницы """
    template_name = 'mail_sender/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['count_mailing'] = MailingSettings.objects.count()  # кол-во рассылок
        context_data['active_mailing'] = MailingSettings.objects.filter(is_active=True).count()  # кол-во активных рассылок
        context_data['uniqe_clients'] = Client.objects.distinct().count()  # кол-во уникальных клиентов
        context_data['blog_content'] = Article.objects.all().order_by('?')[:3]  # случайные статьи из блога
        return context_data


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ Контроллер показывает клиентов пользователя """
    model = Client
    permission_required = 'mail_sender.view_client'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owners=self.request.user)
        return queryset


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Контроллер добавляет нового клиента пользователю """
    model = Client
    form_class = ClientForm
    permission_required = 'mail_sender.add_client'

    def get_success_url(self):
        return reverse('mail_sender:client_list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owners = self.request.user  # владелец
            self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Контроллер для изменения информации о клиенте """
    model = Client
    form_class = ClientForm
    permission_required = 'mail_sender.change_client'

    def get_success_url(self):
        return reverse('mail_sender:client_list')

    def get_object(self, *args, **kwargs):
        client = super().get_object(*args, **kwargs)
        if client.owners == self.request.user:  # проверка на владельца
            return client
        return reverse('mail_sender:client_list')

    def form_valid(self, form):
        if self.object.owners == self.request.user:
            self.object.owners = self.request.user
            self.object.save()
        if form.is_valid():
            self.object = form.save()
            self.object.save()
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """ Контроллер для показа полной информации и клиенте """
    model = Client
    permission_required = 'mail_sender.view_client'


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """ Контроллер для удаления клиента """
    model = Client
    success_url = reverse_lazy('mail_sender:client_list')
    permission_required = 'mail_sender.delete_client'


class MailingSettingsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ Контроллера для показа списка рассылок пользователя """
    model = MailingSettings
    permission_required = 'mail_sender.view_mailingsettings'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='Moderator').exists() or self.request.user.is_superuser:
            return queryset.all()
        queryset = queryset.filter(owners=self.request.user)
        return queryset


class MailingSettingsDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """ Контроллер для показа детальной информации об рассылке """
    model = MailingSettings
    permission_required = 'mail_sender.view_mailingsettings'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        clients = MailingSettings.objects.get(id=self.kwargs.get('pk')).client.all()  # клиенты пользователя
        # print(clients)
        context_data['clients'] = clients
        return context_data


class MailingSettingsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Контроллер для создания рассылки """
    model = MailingSettings
    form_class = MailingSettingsForm
    permission_required = 'mail_sender.add_mailingsettings'

    def get_success_url(self):
        return reverse('mail_sender:mails_list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owners = self.request.user
            self.object.save()
        return super().form_valid(form)


class MailingSettingsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Контроллер для изменения рассылки """
    model = MailingSettings
    permission_required = 'mail_sender.change_mailingsettings'

    def get_success_url(self):
        return reverse('mail_sender:mails_list')

    def get_form_class(self):
        if (self.request.user.has_perm('mail_sender.set_active') and self.request.user.is_staff) \
                or self.request.user.is_superuser:
            return ModeratorMailingSettingsForm
        return MailingSettingsForm

    def form_valid(self, form):
        if self.object.owners == self.request.user:
            self.object.owners = self.request.user
            self.object.save()
            if form.is_valid():
                self.object = form.save()
                self.object.save()
        return super().form_valid(form)


class MailingSettingsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """ Контроллер для удаления рассылки """
    model = MailingSettings
    success_url = reverse_lazy('mail_sender:mails_list')
    permission_required = 'mail_sender.view_mailingsettings'


class PersonalAreaView(LoginRequiredMixin, TemplateView):
    """ Контроллер для отображения Личного кабинета """
    template_name = 'mail_sender/personal_area.html'


class MailingMessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Контроллера для создания сообщения для рассылки """
    model = MailingMessage
    form_class = MailingMessageForm
    permission_required = 'mail_sender.add_mailingmessage'

    def get_success_url(self):
        return reverse('mail_sender:personal_area')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owners = self.request.user
            self.object.save()
            return super().form_valid(form)


class MailingMessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Контроллер для изменения сообщения для рассылки """
    model = MailingMessage
    form_class = MailingMessageForm
    permission_required = 'mail_sender.change_mailingmessage'

    def get_success_url(self):
        return reverse('mail_sender:personal_area')

    def form_valid(self, form):
        if self.object.owners == self.request.user:
            self.object.owners = self.request.user
            self.object.save()
        if form.is_valid():
            self.object = form.save()
            self.object.save()
        return super().form_valid(form)


class MailingMessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ Контроллер для показа списка сообщений """
    model = MailingMessage
    permission_required = 'mail_sender.view_mailingmessage'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owners=self.request.user)  # владелец
        return queryset


class MailingMessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """ Контроллер для показа детальной информации о сообщении """
    model = MailingMessage
    permission_required = 'mail_sender.view_mailingmessage'


class MailingMessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """ Контроллер для удаления сообщения """
    model = MailingMessage
    success_url = reverse_lazy('mail_sender:list_messages')
    permission_required = 'mail_sender.delete_mailingmessage'


class MailingLogListView(LoginRequiredMixin, ListView):
    """ Контроллер для показа списка логов """
    model = MailingLog

