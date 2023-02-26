from django.urls import path
from messages.views import *
from chats.views import my_login_required


urlpatterns = [
    path('api/v1.0/<int:pk>/', my_login_required(ShowMessagesCreateMessage.as_view())),
    path('api/v1.0/messages_cntrf/', messages),
    path('api/v1.0/message/<int:pk>/', my_login_required(EditDeleteMessage.as_view())),
    path('api/v1.0/message/add_reaction/', my_login_required(AddReaction.as_view()), name='add_reaction'),
    path('api/v1.0/message/<int:message_id>/edit_reaction/<int:user_id>/', my_login_required(UpdateDeleteReaction.as_view())),
]
