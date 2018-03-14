from django.db import models
from profile.models import Profile
from django.forms import ModelForm, Textarea


class Message(models.Model):
    profile = models.name = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name="Perfil")
    text = models.TextField(verbose_name="Texto", max_length=140)
    date = models.DateTimeField(verbose_name="Fecha", auto_now=True)

    class Meta:
        verbose_name = "mensaje"
        verbose_name_plural = "mensajes"

    def __str__(self):
        return "@{} · {}".format(self.profile.user, self.date)


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': Textarea(attrs={"class": "form-control", "rows": 3,
                                           "placeholder": "¿Qué te cuentas?", "minlength": 1, "maxlength": 140})}


class Response(models.Model):
    message = models.name = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Mensaje")
    profile = models.name = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name="Perfil")
    text = models.TextField(verbose_name="Texto", max_length=140)
    date = models.DateTimeField(verbose_name="Fecha", auto_now=True)

    class Meta:
        verbose_name = "respuesta"
        verbose_name_plural = "respuestas"

    def __str__(self):
        return "@{} · {}".format(self.profile.user, self.date)


class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': Textarea(attrs={"class": "form-control", "rows": 3,
                                           "placeholder": "Añade una respuesta", "minlength": 1, "maxlength": 140})}
