# Generated by Django 4.0.6 on 2022-09-06 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CustomUsers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sgvuser',
            old_name='user_name',
            new_name='username',
        ),
    ]