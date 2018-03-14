from django.urls import path
from . import views

urlpatterns = [
    path('<username>/', views.public_user, name='public_user'),
    path('<username>/status/<message_id>/',
         views.public_message, name='public_message'),
    path('<username>/message/delete/<message_id>/',
         views.delete_message, name='delete_message'),
]
