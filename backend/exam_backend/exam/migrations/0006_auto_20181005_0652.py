# Generated by Django 2.1.1 on 2018-10-05 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_auto_20181004_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='password',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='username',
        ),
    ]
