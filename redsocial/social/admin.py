from django.contrib import admin
from .models import Message, Relation


class MessageAdmin(admin.ModelAdmin):
    ordering = ['profile', 'date']
    list_display = ['profile', 'date']


# Register your models here.
admin.site.register(Message, MessageAdmin)

# Experimental, no curso
admin.site.register(Relation)
