from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as do_login, logout as do_logout
from .forms import LoginForm


def login(request):

    if request.user.is_authenticated:
        return redirect("home")

    login_form = LoginForm

    if request.method == 'POST':
        login_form = login_form(data=request.POST)
        if login_form.is_valid():
            # Aquí recuperamos al usuario, hacemos el login y redireccioamos
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            do_login(request, user)
            return redirect("home")

    return render(request, 'login/login.html', {'form': login_form})


def logout(request):

    if request.user.is_authenticated:
        do_logout(request)

    return redirect("home")
