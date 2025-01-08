from django.contrib import admin
from .models import AuthUser


@admin.register(AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ('login', 'email', 'first_name', 'last_name', 'created_at')
    search_fields = ('login', 'email', 'first_name', 'last_name')
    readonly_fields = ('id', 'created_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('login', 'email', 'password')
        }),
        ('Персональные данные', {
            'fields': ('first_name', 'last_name')
        }),
        ('Системная информация', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )
