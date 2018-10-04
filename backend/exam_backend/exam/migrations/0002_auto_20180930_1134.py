# Generated by Django 2.1.1 on 2018-09-30 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='audio',
            field=models.FileField(null=True, upload_to='answers_audio/'),
        ),
        migrations.AddField(
            model_name='answer',
            name='hint',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='priority',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='audio',
            field=models.FileField(null=True, upload_to='questions_audio/'),
        ),
        migrations.AddField(
            model_name='question',
            name='questions_number',
            field=models.IntegerField(null=True),
        ),
    ]