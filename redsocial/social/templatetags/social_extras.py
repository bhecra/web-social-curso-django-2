from profile.models import Profile
from django import template
from social.models import Like, Relation

register = template.Library()


@register.simple_tag
def user_has_relation(following_user, follower_user):
    try:
        Relation.objects.get(following__user=following_user,
                             follower__user=follower_user)
        return True
    except Relation.DoesNotExist:
        return False


@register.simple_tag
def user_likes_message(user, message):
    profile = Profile.objects.get(user=user)
    try:
        Like.objects.get(message=message, profile=profile)
        return True
    except Like.DoesNotExist:
        return False


@register.simple_tag
def user_recommended(user):
    # Recuperamos al usuario
    profile = Profile.objects.get(user=user)
    # Recuperamos todos los perfiles excluyendo a uno mismo y a los que ya seguimos
    profiles_list = Profile.objects.all().exclude(
        user=user).exclude(id__in=profile.follower_set.values("following_id"))
    # Recreamos la lista de perfiles haciendo mapeo ordenado por número de seguidores
    profiles_list = sorted(profiles_list,
                           key=lambda p: len(p.following_set.all()),
                           reverse=True)  # Por defecto es de menor a mayor
    # Devolvemos los 4 primeros
    return profiles_list[:4]
