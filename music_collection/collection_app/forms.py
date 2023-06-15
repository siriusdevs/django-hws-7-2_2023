from django.forms import ChoiceField, Form, DecimalField, CharField, EmailField
from .config import DECIMAL_MAX_DIGITS, DECIMAL_PLACES, CF_DEFAULT, EMAIL_LENGTH
from django.contrib.auth import forms as auth_forms, models as auth_models
from django import forms
from .models import Artists


class AddFundsForm(Form):
    money = DecimalField(
        label='Amount',
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
    )


class RegistrationForm(auth_forms.UserCreationForm):
    first_name = CharField(max_length=CF_DEFAULT, required=True)
    last_name = CharField(max_length=CF_DEFAULT, required=True)
    email = EmailField(max_length=EMAIL_LENGTH, required=True)

    class Meta:
        model = auth_models.User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

class ArtistPostForm(Form):
    class Meta:
        model = Artists
        fields = ('name', 'birth_date', 'country', 'education')

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
        'birth_date': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
        'country': forms.Select(attrs={'class': 'form-control'}),
        'education': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
    }
