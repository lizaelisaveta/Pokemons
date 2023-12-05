from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control;"}))


User = get_user_model()
class UserCreationForm(UserCreationForm):
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[],
        error_messages={
            "unique": ("A user with that username already exists."),
        },
        null=True,
        blank=True,
    )

    first_name = models.CharField(("first name"), max_length=150, blank=True)
    last_name = models.CharField(("last name"), max_length=150, blank=True)
    email = models.EmailField(("email address"), unique=True, )
    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        ("active"),
        default=False,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(("date joined"), default=timezone.now)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', )
