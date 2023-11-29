from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control;"}))

