from django import forms

from account.models import UserBase
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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
        model = UserBase
        fields = ['email', 'password']


class AddressCheckoutForm(forms.ModelForm):

    first_name = forms.CharField(required=False)
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
            Submit('submit', 'Submit', css_class='btn btn-primary btn-block py-2 mb-4 mt-5 fw500 w-100'))

    class Meta:
        model = UserBase
        fields = ['first_name',
                  'address', 'city', 'province', 'zipcode']
