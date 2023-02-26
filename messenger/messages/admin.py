from django.contrib import admin
from messages.models import Message, Reaction, UserReaction

# Register your models here.
admin.site.register(Message)
admin.site.register(Reaction)
admin.site.register(UserReaction)
