from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User # Removed ActivityLog import

# Define a custom User admin if you need to customize display/fields
# For now, we can use the default UserAdmin structure with our custom model
class UserAdmin(BaseUserAdmin):
    # Add any customizations here if needed in the future
    # For example, list_display = ('username', 'email', 'is_staff', 'streak')
    pass

# Register your models here.
admin.site.register(User, UserAdmin)
# Removed ActivityLog registration
