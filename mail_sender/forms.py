from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from mail_sender.models import Client, MailingSettings, MailingMessage


class CrispyFormMixin(forms.Form):
    """ Миксин для оформления форм в стиле crispy. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))


class ClientForm(CrispyFormMixin, forms.ModelForm):
    """ Форма для Client. """
    class Meta:
        model = Client
        fields = '__all__'


class MailingSettingsForm(CrispyFormMixin, forms.ModelForm):
    """ Форма для MailingSettings. """
    class Meta:
        model = MailingSettings
        fields = '__all__'


class MailingMessageForm(CrispyFormMixin, forms.ModelForm):
    """ Форма для MailingMessage. """
    class Meta:
        model = MailingMessage
        fields = '__all__'
