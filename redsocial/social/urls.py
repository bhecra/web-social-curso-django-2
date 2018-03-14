from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.public_search,
         name='public_search'),  # Arriba del todo
    path('<username>/', views.user_messages, name='user_messages'),
    path('<username>/responses/', views.user_responses, name='user_responses'),
    path('<username>/following/', views.user_following, name='user_following'),
    path('<username>/followers/', views.user_followers, name='user_followers'),
    path('<username>/likes/', views.user_likes, name='user_likes'),
    path('<username>/status/<message_id>/',
         views.public_message, name='public_message'),
    path('<username>/message/delete/<message_id>/',
         views.ajax_delete_message, name='ajax_delete_message'),
    path('<username>/response/delete/<response_id>/',
         views.ajax_delete_response, name='ajax_delete_response'),
    path('<username>/message/like/<message_id>/',
         views.ajax_toggle_like, name="ajax_toggle_like"),
]
