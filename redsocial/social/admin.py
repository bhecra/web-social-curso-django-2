from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    ordering = ['profile', 'date']
    list_display = ['profile', 'date']


# Register your models here.
admin.site.register(Message, MessageAdmin)
