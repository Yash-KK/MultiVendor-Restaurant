from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#MODELS
from .models import (
    User,
    UserProfile
)

# register the models here

class AdminUser(UserAdmin):
    list_display = ['email','first_name', 'last_name', 'username', 'is_active','role','date_joined']
    list_display_links = ['email']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, AdminUser)
admin.site.register(UserProfile)

