# Generated by Django 2.1.1 on 2020-02-05 20:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exam_manage', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_number', models.IntegerField(null=True)),
                ('finished', models.BooleanField(default=False)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam_manage.Course')),
                ('mode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam_manage.StrictMode')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SessionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blocked', models.BooleanField(default=False)),
                ('current_result', models.IntegerField(null=True)),
                ('will_send_hint', models.BooleanField(default=False)),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam_manage.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='SessionQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.IntegerField(null=True)),
                ('result', models.IntegerField(null=True)),
                ('attempts_number', models.IntegerField(null=True)),
                ('finished', models.BooleanField(default=False)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam_manage.Question')),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.CourseSession')),
            ],
        ),
        migrations.AddField(
            model_name='sessionanswer',
            name='sessionQuestion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.SessionQuestion'),
        ),
    ]