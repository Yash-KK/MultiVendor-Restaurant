# Generated by Django 4.1.2 on 2022-10-23 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='address_line_1',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='address_line_2',
        ),
    ]
