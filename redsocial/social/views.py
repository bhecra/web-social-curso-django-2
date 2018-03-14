from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from profile.models import Profile
from django.contrib.auth.models import User
from .models import Message, MessageForm, Response, ResponseForm


def home_logged(request):
    profile = Profile.objects.get(user=request.user)
    profile.set_in_session(request)
    messages = Message.objects.filter(profile=profile).order_by('-date')[:20]
    for i in range(len(messages)):
        messages[i].responses = Response.objects.filter(
            message=messages[i]).count()

    message_form = MessageForm()
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.profile = profile
            message.save()
            return redirect('/')

    return render(request, 'social/home_logged.html', {'messages': messages, 'form': message_form})


def public_user(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    messages = Message.objects.filter(profile=profile).order_by('-date')[:20]
    for i in range(len(messages)):
        messages[i].responses = Response.objects.filter(
            message=messages[i]).count()

    return render(request, 'social/public_user.html', {'user': user, 'profile': profile, 'messages': messages})


def public_message(request, username, message_id):
    message = get_object_or_404(Message, pk=message_id)
    if message.profile.user.username != username:
        raise Http404("Mensaje no se ha encontrado")
    responses = Response.objects.filter(message=message).order_by('date')

    response_form = ResponseForm()
    if request.user.is_authenticated and request.method == 'POST':
        response_form = ResponseForm(request.POST)
        if response_form.is_valid():
            response = response_form.save(commit=False)
            response.message = message
            response.profile = message.profile
            response.save()
            return redirect('/{}/status/{}/#r-{}'.format(message.profile.user, message.id, response.id))

    return render(request, 'social/public_message.html', {'message': message, 'responses': responses,
                                                          'form': response_form})


def delete_message(request, username, message_id):
    # Creamos la respuesta inicialmente vacía
    response = {'status': 'none'}
    try:
        message = Message.objects.get(pk=message_id)
        if request.user.is_authenticated and request.user == message.profile.user:
            message.delete()
            # Todo bien, respuesta afirmativa
            response['status'] = 'success'
    except:
        # Algo falló, respuesta negativa
        response['status'] = 'fail'
    finally:
        return JsonResponse(response, safe=False)
