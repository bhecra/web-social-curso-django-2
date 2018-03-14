from profile.models import Profile
from django.db import models
from django.forms import ModelForm, Textarea


class Message(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name="Perfil")
    text = models.TextField(verbose_name="Texto", max_length=140)
    date = models.DateTimeField(verbose_name="Fecha", auto_now=True)

    class Meta:
        verbose_name = "mensaje"
        verbose_name_plural = "mensajes"
        ordering = ['-date']

    def __str__(self):
        return "@{} · {}".format(self.profile.user, self.date)


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': Textarea(attrs={"class": "form-control", "rows": 3,
                                           "placeholder": "¿Qué te cuentas?",
                                           "minlength": 1, "maxlength": 140})}


class Response(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Mensaje")
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name="Perfil")
    text = models.TextField(verbose_name="Texto", max_length=140)
    date = models.DateTimeField(verbose_name="Fecha", auto_now=True)

    class Meta:
        verbose_name = "respuesta"
        verbose_name_plural = "respuestas"
        ordering = ['-date']

    def __str__(self):
        return "@{} · {}".format(self.profile.user, self.date)


class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': Textarea(attrs={"class": "form-control", "rows": 3,
                                           "placeholder": "Añade una respuesta",
                                           "minlength": 1, "maxlength": 140})}


class Relation(models.Model):
    following = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="following_set")
    follower = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="follower_set")
    date = models.DateTimeField(
        verbose_name="Fecha", auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = ('following', 'follower')
        ordering = ['-date']


class Like(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('profile', 'message')
        ordering = ['-date']
