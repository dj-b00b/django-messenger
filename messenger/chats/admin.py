from django.contrib import admin
from chats.models import Chat, Category, ChatMember

# Register your models here.
admin.site.register(Chat)
admin.site.register(Category)
admin.site.register(ChatMember)
