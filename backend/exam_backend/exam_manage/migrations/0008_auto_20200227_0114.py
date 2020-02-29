# Generated by Django 2.1.1 on 2020-02-26 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_manage', '0007_auto_20200227_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='bad_audio_url',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='good_audio_url',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='perfect_audio_url',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='satisfactory_audio_url',
            field=models.CharField(max_length=512, null=True),
        ),
    ]