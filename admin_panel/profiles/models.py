import uuid
from django.db import models


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login = models.CharField('login', max_length=255)
    email = models.TextField('email', blank=True)
    phone = models.TextField('phone', blank=True)
    password = models.TextField('password', blank=True)
    first_name = models.TextField('first_name', blank=True)
    last_name = models.TextField('last_name', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "auth\".\"users"
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

