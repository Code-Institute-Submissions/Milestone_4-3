from django.contrib import admin
from .models import UserProfile

class UserAdmin(admin.ModelAdmin):
    list_display = ('default_type', 'default_phone_number')

admin.site.register(UserProfile, UserAdmin)

