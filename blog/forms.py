from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from blog.models import Article


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


class ArticleForm(CrispyFormMixin, forms.ModelForm):
    """ Форма для Client. """

    class Meta:
        model = Article
        fields = '__all__'
