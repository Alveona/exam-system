# Generated by Django 2.1.1 on 2020-02-25 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam_auth', '0003_auto_20200208_2247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='access_group',
        ),
    ]
