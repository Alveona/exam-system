# Generated by Django 2.1.1 on 2020-02-08 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_auth', '0002_profile_access_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='group',
            field=models.IntegerField(choices=[(0, 'student'), (1, 'teacher'), (2, 'admin')], default=0),
        ),
    ]
