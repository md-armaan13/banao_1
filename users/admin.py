from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users ,Profile

admin.site.register(Users, UserAdmin)

admin.site.register(Profile)