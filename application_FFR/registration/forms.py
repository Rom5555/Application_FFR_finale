from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'S\'inscrire',css_class='button is-info'))
        self.helper.layout = Layout(
            Field('first_name', css_class='input'),
            Field('last_name', css_class='input'),
            Field('username', css_class='input'),
            Field('email', css_class='input'),
            Field('password1', css_class='input'),
            Field('password2', css_class='input'),

        )