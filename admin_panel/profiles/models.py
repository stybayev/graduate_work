import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    permissions = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "auth\".\"roles"

    def __str__(self):
        return f"<Role {self.name}>"


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def get_roles(self):
        # Метод для получения ролей пользователя
        return ", ".join([role.name for role in self.profile.roles.all()])

    class Meta:
        db_table = "auth_user"
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('profiles.CustomUser', on_delete=models.CASCADE, related_name='profile')
    phone = models.TextField('phone', blank=True)
    roles = models.ManyToManyField(Role, through='UserRole', blank=True)

    class Meta:
        unique_together = ('user', 'phone')
        db_table = "auth\".\"profiles"
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"{self.user.username}"


class UserRole(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = "auth\".\"user_roles"
        unique_together = ('user', 'role')

    def __str__(self):
        return f"<UserRole user={self.user.user}, role={self.role.name}>"
