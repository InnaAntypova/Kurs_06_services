from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.forms import HiddenInput


from mail_sender.forms import CrispyFormMixin
from users.models import User


class UserForm(CrispyFormMixin, UserChangeForm):
    """ Форма для Пользователя """
    class Meta:
        model = User
        fields = '__all__'


class RegisterForm(CrispyFormMixin, UserCreationForm):
    """  Форма для регистрации Пользователя """
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(CrispyFormMixin, UserChangeForm):
    """ Форма для Профиля пользователя """
    class Meta:
        model = User
        fields = ('email', 'password', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = HiddenInput()


class UserForgotPasswordForm(PasswordResetForm):
    pass


class UserSetNewPasswordForm(SetPasswordForm):
    pass


class ModeratorForm(CrispyFormMixin, forms.ModelForm):
    """ Форма для Модератора """
    class Meta:
        model = User
        fields = ['is_active']
