from dataclasses import field, fields
from datetime import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, modelform_factory

from store.models import Customer


class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login'))

    class Meta:
        model = User
        fields = ['username', 'password']


class RegisterForm(forms.Form):

    username = forms.CharField()


class RegisterUser(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name',
                  'email', 'password1', 'password2']

        help_texts = {
            'username': None,
            'email': None,
            'password': None,
        }
