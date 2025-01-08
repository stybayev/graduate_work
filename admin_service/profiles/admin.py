from django.contrib import admin
from .models import UserProfile
from werkzeug.security import generate_password_hash


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'created_at', 'updated_at')
    search_fields = ('full_name', 'phone_number')
    readonly_fields = ('id', 'user_id', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('profiles.view_userprofile')

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
