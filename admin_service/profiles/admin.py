from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'created_at', 'updated_at')
    search_fields = ('full_name', 'phone_number')
    readonly_fields = ('id', 'user_id', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def has_view_permission(self, request, obj=None):
        # Проверяем наличие специального разрешения на просмотр профилей
        return request.user.has_perm('profiles.view_userprofile')

    def has_change_permission(self, request, obj=None):
        # Запрещаем изменение профилей через админку
        return False

    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление профилей через админку
        return False

    def has_add_permission(self, request):
        # Запрещаем создание профилей через админку
        return False
