from django.contrib import admin
from .models import CustomUser, UserItems

admin.site.register(CustomUser)
admin.site.register(UserItems)