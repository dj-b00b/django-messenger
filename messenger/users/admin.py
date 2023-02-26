from django.contrib import admin
from users.models import User, UserSession, Contact

# Register your models here.
admin.site.register(User)
admin.site.register(UserSession)
admin.site.register(Contact)

