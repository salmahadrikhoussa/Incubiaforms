from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'city', 'project_name', 'project_level', 'industry', 'choice')

admin.site.register(User,UserAdmin)
