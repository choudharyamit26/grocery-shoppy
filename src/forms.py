from django import forms
from .models import User, Address

ADDRESS_TYPE = (
    ('Office', 'Office'),
    ('Home', 'Home'),
    ('Commercial', 'Commercial'),
)


class SignUpForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


class AddressForm(forms.Form):
    add_name = forms.CharField()
    mobile_number = forms.IntegerField()
    landmark = forms.CharField()
    city = forms.CharField()
    address_type = forms.CharField()
