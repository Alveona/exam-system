# Generated by Django 2.1.1 on 2018-09-30 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_auto_20180930_1134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='questions_number',
            new_name='answers_number',
        ),
    ]
