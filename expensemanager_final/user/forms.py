from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.db import transaction


class ManagerRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'age',  'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_manager = True
        user.save()
        return user


class ClientRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        exclude = ['User']
        fields = ['username', 'first_name', 'last_name', 'email', 'age',  'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_client = True
        user.save()
        return user
