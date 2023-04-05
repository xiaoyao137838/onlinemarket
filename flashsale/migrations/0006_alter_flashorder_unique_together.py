# Generated by Django 4.1.6 on 2023-04-04 13:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flashsale', '0005_alter_flashsale_available_qty'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='flashorder',
            unique_together={('customer', 'flash_sale')},
        ),
    ]
