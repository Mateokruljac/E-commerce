from django.db import migrations



def create_admin_customer(apps, schema_editor):
    from django.contrib.auth.models import User
    from store.models import Customer

    # Create a superuser
    Customer.objects.create(
        user = User.objects.get(username="admin"),
        name='admin',
        email='admin@example.com',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_create_superuser'),
    ]

    operations = [
        migrations.RunPython(create_admin_customer),
    ]
