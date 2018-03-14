from django.shortcuts import render
from social.views import home_logged


def home(request):
    if request.user.is_authenticated:
        return home_logged(request)
    return render(request, 'base/home.html')


def about(request):
    return render(request, 'base/about.html')
