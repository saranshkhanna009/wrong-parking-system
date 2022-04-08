from re import I
from django.contrib import admin

# Register your models here.
from .models import User, UserOTP
admin.site.register(User)
admin.site.register(UserOTP)
