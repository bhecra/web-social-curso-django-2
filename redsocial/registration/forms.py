from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re


class SignUpForm(forms.Form):

    username = forms.CharField(label='', min_length=4, max_length=16, widget=forms.TextInput(
        attrs={'placeholder': 'Escribe tu usuario', 'class': 'form-control'}))
    password1 = forms.CharField(label='', min_length=8, max_length=30, widget=forms.PasswordInput(
        attrs={'placeholder': 'Nueva contraseña', 'class': 'form-control'}))
    password2 = forms.CharField(label='', min_length=8, max_length=30, validators=[], widget=forms.PasswordInput(
        attrs={'placeholder': 'Repite la contraseña', 'class': 'form-control'}))

    def clean(self):

        username = self.cleaned_data['username']

        pattern = '^[a-zA-Z0-9]*$'
        if not re.match(pattern, username):
            self.add_error(
                'username', 'El nombre de usuario sólo puede contener letras y números.')

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        else:
            self.add_error(
                'username', 'Ya existe un usuario con este nombre.')

        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            self.add_error('password1', 'Las contraseñas no concuerdan.')

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'], password=self.cleaned_data['password1'])
        user.save()

        return user
