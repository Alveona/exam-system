# Generated by Django 2.1.1 on 2018-10-06 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursesession',
            old_name='attempts_number',
            new_name='attempt_number',
        ),
        migrations.AddField(
            model_name='course',
            name='attempts',
            field=models.IntegerField(null=True),
        ),
    ]