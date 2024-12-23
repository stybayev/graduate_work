from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, CustomUser, Role, UserRole
from .forms import ProfileForm


class ProfileInline(admin.StackedInline):
    model = Profile
    form = ProfileForm
    can_delete = False
    verbose_name_plural = "Профили"
    fk_name = 'user'  # Связь с пользователем

    # Отображение ролей
    readonly_fields = ('get_roles',)

    def get_roles(self, obj):
        return ", ".join([role.name for role in obj.roles.all()])

    get_roles.short_description = 'Роли'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    model = CustomUser

    list_display = ('username', 'email', 'first_name', 'last_name', 'get_roles', 'is_active')

    def get_roles(self, obj):
        return obj.get_roles()

    get_roles.short_description = 'Роли'

    # Поля для редактирования
    fieldsets = UserAdmin.fieldsets + (
        ('Роли', {
            'fields': (),
        }),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


admin.site.register(Role)
admin.site.register(UserRole)
