from django.db import migrations


def create_superuser(apps, schema_editor):
    from django.contrib.auth.models import User

    # Create a superuser
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
