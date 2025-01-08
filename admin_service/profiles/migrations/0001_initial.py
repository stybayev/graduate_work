from django.db import migrations
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


def create_custom_permissions(apps, schema_editor):
    content_type, _ = ContentType.objects.get_or_create(
        app_label='profiles',
        model='userprofile'
    )

    Permission.objects.get_or_create(
        codename='view_userprofile',
        name='Can view user profile',
        content_type=content_type,
    )


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(create_custom_permissions),
    ]
