# Generated by Django 2.1.1 on 2018-10-05 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0006_auto_20181005_0652'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='token',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
