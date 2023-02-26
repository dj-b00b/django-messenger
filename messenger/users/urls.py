from django.urls import path
from users.views import *
from chats.views import my_login_required


urlpatterns = [
    path('api/v1.0/user/<int:pk>/', my_login_required(ShowInfoRemoveChangeDelUser.as_view())),
    path('api/v1.0/user/<int:user_id>/show_contacts/', my_login_required(ShowContactsAddContact.as_view())),
    path('api/v1.0/user/<int:user_id>/del_contact/<int:friend_id>/', my_login_required(DelContact.as_view()), name='del_user_from_contacts')
]
