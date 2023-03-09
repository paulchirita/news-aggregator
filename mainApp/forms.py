from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import AppUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = AppUser
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]