# Generated by Django 2.1.1 on 2018-12-12 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_auto_20181213_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
