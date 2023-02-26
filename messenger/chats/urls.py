from django.urls import path
from chats.views import *


urlpatterns = [
    path('api/v1.0/<int:pk>/', ShowChatsCreateChat.as_view()),  # тут стоял декоратор для авторизации!
    path('api/v1.0/chat/<int:pk>/', ShowEditDeleteChat.as_view()),  # декоратор тоже поставить !
    path('api/v1.0/chat/<int:pk>/members/', my_login_required(ShowChatMembersAddChatMember.as_view())),
    path('api/v1.0/chat/<int:chat_id>/del_member/<int:user_id>/', my_login_required(DelChatMember.as_view()), name='del_chat_member'), 
    path('api/v1.0/chat/<int:chat_id>/admin/<int:user_id>/', my_login_required(AddRemoveAdmin.as_view()))
]
