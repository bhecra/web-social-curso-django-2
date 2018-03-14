from django.contrib import admin
from .models import Profile
from social.models import Message


class MessageInline(admin.StackedInline):
    model = Message
    ordering = ['-date']
    extra = 0


class ProfileAdmin(admin.ModelAdmin):
    ordering = ['user']
    list_display = ['user', 'alias']

    inlines = [
        MessageInline,
    ]


admin.site.register(Profile, ProfileAdmin)
