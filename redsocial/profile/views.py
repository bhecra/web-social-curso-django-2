from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Profile


def profile(request):

    if not request.user.is_authenticated:
        return redirect("home")

    # Comprobamos si el usuario tiene un perfil, si no es así se lo creamos
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
        profile.save()

    profile_form = ProfileForm(
        initial={'alias': profile.alias, 'email': profile.email, 'description': profile.description,
                 'link': profile.link, 'avatar': profile.avatar})

    if request.method == 'POST':
        profile_form = ProfileForm(data=request.POST, files=request.FILES)
        if profile_form.is_valid():
            # Aquí editaremos el perfil y recargamos la página
            profile_form.save(profile)
            # Pero antes no olvidemos volver a guardar el perfil en la sesión
            profile.set_in_session(request)
            return redirect("profile")

    return render(request, 'profile/profile.html', {'form': profile_form})
