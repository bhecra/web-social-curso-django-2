from profile.models import Profile
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Message, MessageForm, Response, ResponseForm, Relation, Like


def home_logged(request):
    profile = Profile.objects.get(user=request.user)
    profile.set_in_session(request)

    message_form = MessageForm()
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.profile = profile
            message.save()
            return redirect('/')

    # Recuperamos los mensajes del perfil
    profile_messages = profile.message_set.all()
    # Recuperamos los mensajes marcados con me gusta
    like_messages = Message.objects.filter(
        id__in=profile.like_set.values('message_id'))
    messages = (profile_messages | like_messages)
    # Para cada usuario que seguimos sumamos sus mensajes
    for relation in profile.follower_set.all():
        relation_messages = relation.following.message_set.all()
        messages = messages | relation_messages

    messages = messages.order_by("-date")
    paginator = Paginator(messages, 4)
    page = request.GET.get('page')
    messages = paginator.get_page(page)

    return render(request, 'social/home_logged.html', {'messages': messages,
                                                       'profile': profile,
                                                       'form': message_form})


def user_messages(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    paginator = Paginator(profile.message_set.all().order_by("-date"), 4)
    page = request.GET.get('page')
    messages = paginator.get_page(page)

    # Si el usuario actual está identificado recuperamos su perfil
    if request.user.is_authenticated:
        follower = Profile.objects.get(user=request.user)
        # Comprobamos si hay una petición POST para cambiar el seguimiento
        if request.method == 'POST':
            try:
                # Si existe el seguimiento lo borramos y si no lo creamos
                Relation.objects.get(
                    following=profile, follower=follower).delete()
            except Relation.DoesNotExist:
                Relation.objects.create(
                    following=profile, follower=follower)
            # Finalmente hacemos la redirección para actualizar y prevenir reenvíos
            return redirect('/{}'.format(profile.user.username))

    return render(request, 'social/user_messages.html', {'messages': messages, 'profile': profile})


def user_responses(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    paginator = Paginator(profile.response_set.all().order_by("-date"), 4)
    page = request.GET.get('page')
    responses = paginator.get_page(page)

    return render(request, 'social/user_responses.html', {'profile': profile,
                                                          'responses': responses})


def user_following(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    relations_list = Relation.objects.filter(
        follower=profile).order_by('-date')
    paginator = Paginator(relations_list, 4)
    page = request.GET.get('page')
    relations = paginator.get_page(page)

    return render(request, 'social/user_following.html', {'profile': profile,
                                                          'relations': relations})


def user_followers(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    relations_list = Relation.objects.filter(
        following=profile).order_by('-date')
    paginator = Paginator(relations_list, 4)
    page = request.GET.get('page')
    relations = paginator.get_page(page)

    return render(request, 'social/user_followers.html', {'profile': profile,
                                                          'relations': relations})


def user_likes(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    paginator = Paginator(profile.like_set.all().order_by("-date"), 4)
    page = request.GET.get('page')
    likes = paginator.get_page(page)

    return render(request, 'social/user_likes.html', {'likes': likes, 'profile': profile})


def public_message(request, username, message_id):
    message = get_object_or_404(Message, pk=message_id)
    if message.profile.user.username != username:
        raise Http404("Mensaje no se ha encontrado")

    response_form = ResponseForm()
    if request.user.is_authenticated and request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        response_form = ResponseForm(request.POST)
        if response_form.is_valid():
            response = response_form.save(commit=False)
            response.message = message
            response.profile = profile
            response.save()
            return redirect('/{}/status/{}/#r-{}'.format(message.profile.user,
                                                         message.id,
                                                         response.id))

    return render(request, 'social/public_message.html', {'message': message,
                                                          'form': response_form})


def ajax_delete_message(request, username, message_id):
    if request.is_ajax():
        # Creamos la respuesta inicialmente vacía
        response_json = {'status': 'none'}
        try:
            message = Message.objects.get(pk=message_id)
            if request.user.is_authenticated and request.user == message.profile.user:
                message.delete()
                # Todo bien, respuesta afirmativa
                response_json['status'] = 'success'
        except Message.DoesNotExist:
            # Algo falló, respuesta negativa
            response_json['status'] = 'fail'

        return JsonResponse(response_json, safe=False)


def ajax_delete_response(request, username, response_id):
    if request.is_ajax():
        # Creamos la respuesta inicialmente vacía
        response_json = {'status': 'none'}
        try:
            response = Response.objects.get(pk=response_id)
            if request.user.is_authenticated and request.user == response.profile.user:
                response.delete()
                # Todo bien, respuesta afirmativa
                response_json['status'] = 'success'
        except Message.DoesNotExist:
            # Algo falló, respuesta negativa
            response_json['status'] = 'fail'

        return JsonResponse(response_json, safe=False)


def ajax_toggle_like(request, username, message_id):
    if request.is_ajax():
        # Recuperamos el mensaje
        message = Message.objects.get(pk=message_id)

        # Creamos una respuesta genérica
        response_json = {'status': 'fail', 'action': 'null', 'likes': 0}

        if request.user.is_authenticated:
            # Recuperamos el perfil del usuario autenticado
            profile = Profile.objects.get(user=request.user)
            try:
                # Si el like existe lo borramos e indicamos la acción dislike
                Like.objects.get(message=message, profile=profile).delete()
                response_json['action'] = "dislike"
            except Like.DoesNotExist:
                # Si no existe lo creamos e indicamos la acción like
                Like.objects.create(message=message, profile=profile)
                response_json['action'] = "like"

        # Actualizamos el número de likes
        response_json['status'] = 'success'
        response_json['likes'] = message.like_set.all().count()

        return JsonResponse(response_json, safe=False)


def public_search(request):
    q = request.GET.get('q')
    profiles = Profile.objects.filter(
        Q(user__username__contains=q) | Q(alias__contains=q))
    return render(request, 'social/public_search.html', {'profiles': profiles})
