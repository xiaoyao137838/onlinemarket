# Generated by Django 4.1.6 on 2023-04-04 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashsale', '0006_alter_flashorder_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='flashorder',
            unique_together=set(),
        ),
    ]
