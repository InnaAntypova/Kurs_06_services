from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView

from users.forms import RegisterForm, UserForgotPasswordForm, UserSetNewPasswordForm, UserProfileForm, ModeratorForm
from users.models import User

from users.services import send_verify_email


class LoginView(BaseLoginView):
    """ Контроллера Входа(Login) """
    template_name = 'users/login.html'


def logout_user(request):
    """ Контроллер Выхода """
    logout(request)
    return redirect('mail_sender:index')


class RegisterUserView(CreateView):
    """ Контроллер для регистрации пользователя """
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('mail_sender:index')

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            send_verify_email(user)

        return super().form_valid(form)


class ConfirmVerifyUser(View):
    """ Верификация пользователя. """
    def get(self, request, uuid):
        try:
            user = User.objects.get(field_uuid=uuid)
            user.is_active = True
            user.save()

            # создать группу и добавить пользователя в нее с правами
            users_group, created = Group.objects.get_or_create(name='Users')
            if created:
                permissions = Permission.objects.filter(
                    codename__in=['add_client', 'change_client', 'view_client', 'delete_client',
                                  'view_mailingsettings', 'add_mailingsettings', 'change_mailingsettings',
                                  'delete_mailingsettings',
                                  'add_mailingmessage', 'change_mailingmessage', 'view_mailingmessage',
                                  'delete_mailingmessage',
                                  'view_mailinglog']
                )
                users_group.permissions.set(permissions)
            user.groups.add(users_group)
            user.save()

            return render(request, 'users/confirm_register.html')
        except User.DoesNotExist:
            return render(request, 'users/error_register.html')


class UserForgotPasswordView(PasswordResetView):
    """ Контроллер для восстановления забытого пароля """
    form_class = UserForgotPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('mail_sender:index')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/password_subject_reset_mail.txt'
    email_template_name = 'users/password_reset_mail.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """ Контроллер для подтверждения нового пароля """
    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'


class UserProfileView(LoginRequiredMixin, UpdateView):
    """ Контроллер для Профиля пользователя """
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user


class ModeratorListView(LoginRequiredMixin, ListView):
    """ Контроллер для отображения всех пользователей для Модератора """
    model = User

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='Moderator').exists() or self.request.user.is_superuser:
            return queryset


class ModeratorUpdateUserView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Контроллер для управления статусом Пользователя """
    model = User
    form_class = ModeratorForm
    permission_required = 'users.set_active'

    def get_object(self, *args, **kwargs):
        user = super().get_object(*args, **kwargs)
        if (self.request.user.has_perm(self.permission_required) and self.request.user.is_staff) \
                or self.request.user.is_superuser:
            return user
        raise PermissionError

    def form_valid(self, form):
        if form.has_changed():
            user = self.get_object()
            if user.is_active:
                user.is_active = False
            user.is_active = True
            user.save()
            form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:all_user')
