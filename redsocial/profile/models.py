from django.db import models
from django.contrib.auth.models import User


def upload_to(instance, filename):
    return "avatars/{}/{}".format(instance.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alias = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    link = models.URLField(max_length=150, null=True, blank=True)
    avatar = models.ImageField(upload_to=upload_to, null=True, blank=True)

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfiles"

    def __str__(self):
        return "@{} {}".format(self.user, self.alias)

    def set_in_session(self, request):
        data = {}
        data['alias'] = self.alias
        data['email'] = self.email
        data['description'] = self.description
        data['link'] = self.link
        data['avatar'] = str(self.avatar)
        request.session['profile'] = data
