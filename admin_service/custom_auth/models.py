from django.db import models
import uuid


class AuthUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login = models.CharField(max_length=255, unique=True)
    email = models.EmailField(null=True, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'auth"."users'
        verbose_name = 'Пользователь Auth'
        verbose_name_plural = 'Пользователи Auth'
