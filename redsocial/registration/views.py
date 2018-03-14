from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm


def signup(request):

    if request.user.is_authenticated:
        return redirect("home")

    signup_form = SignUpForm

    if request.method == 'POST':
        signup_form = signup_form(data=request.POST)
        if signup_form.is_valid():
            # Aquí registraremos al usuario y haremos la redirección
            user = signup_form.save()
            login(request, user)
            return redirect("profile")

    return render(request, 'registration/signup.html', {'form': signup_form})
