from dataclasses import Field, field, fields
from datetime import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, modelform_factory

from store.models import Customer


class LoginForm(forms.Form):

    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit', 'Login', css_class='btn btn-primary btn-block py-2 mb-4 mt-5 fw500 w-100'))

    class Meta:
        model = User
        fields = ['email', 'password']


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        label='Enter username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
                             'required': 'Email is needed'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('user_name', 'email')

    def clean_user_name(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = User.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit(
            'submit', 'Register', css_class="btn btn-primary btn-block py-2 mb-4 mt-5"))


# class RegisterUser(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('submit', 'Register'))

#     class Meta:
#         model = User
#         fields = ['username', 'last_name', 'first_name',
#                   'email', 'password1', 'password2']

#         help_texts = {
#             'username': None,
#             'email': None,
#             'password': None,
#         }
