from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):

    username = forms.CharField(label='', min_length=3, max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Escribe tu usuario', 'class': 'form-control'}))
    password = forms.CharField(label='', min_length=8, max_length=30, widget=forms.PasswordInput(
        attrs={'placeholder': 'Escribe tu contraseña', 'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("El usuario no existe")
