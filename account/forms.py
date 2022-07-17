from django import forms
from django.contrib.auth.models import User

from .models import Addresses, Customer
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit


class AddressForm(forms.ModelForm):
    is_default = forms.BooleanField()

    class Meta:
        model = Addresses
        fields = ['full_name', 'phone', 'address_line',
                  'address_line2', 'city', 'province', 'zipcode', 'is_default']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit', 'Submit', css_class='btn btn-primary btn-block py-2 mb-4 mt-5 fw500 w-100 '))


class LoginForm(forms.ModelForm):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit', 'Login', css_class='btn btn-primary btn-block py-2 mb-4 mt-5 fw500 w-100'))

    class Meta:
        model = Customer
        fields = ['email', 'password']


class DashboardEditForm(forms.ModelForm):

    email = forms.EmailField(widget=forms.TextInput(
        attrs={"readonly": True, "placeholder": "email"}), required=True)
    user_name = forms.CharField(widget=forms.TextInput(
        attrs={"readonly": True}), required=True)
    #password = forms.CharField(widget=forms.PasswordInput,)
    first_name = forms.CharField(required=False)
    about = forms.CharField(
        max_length=150, widget=forms.Textarea(attrs={"placeholder": "Description about you..."}), required=False)
    address = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"placeholder": "House No, Lot No., Street Name... "}))
    city = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"placeholder": "City or Municipality Name..."}))
    province = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"placeholder": "Province Name..."}))
    zipcode = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"placeholder": "Area code..."}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit', 'Update', css_class='btn btn-primary btn-block py-2 mb-4 mt-5 fw500 w-100'))

    class Meta:
        model = Customer
        fields = ['email', 'user_name', 'first_name', 'about',
                  'address', 'city', 'province', 'zipcode']


class RegistrationForm(forms.ModelForm):
    name = forms.CharField(
        label='Enter username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Email is needed'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('name', 'email')

    def clean_user_name(self):
        user_name = self.cleaned_data['name'].lower()
        r = Customer.objects.filter(name=user_name)
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
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Email', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Repeat Password'})
