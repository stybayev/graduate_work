import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('login', models.EmailField(max_length=255, unique=True, verbose_name='login')),
                ('password', models.CharField(max_length=255, verbose_name='password')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='last name')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
