from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    answer_type = models.IntegerField(verbose_name='Тип вопроса')
    image = models.ImageField(upload_to='questions/', null=True, verbose_name='Изображение')
    difficulty = models.IntegerField(verbose_name='Сложность')
    comment = models.CharField(max_length=255, blank=True)
    answers_number = models.IntegerField(null=True)
    audio = models.FileField(upload_to='questions_audio/', null=True)
    attempts_number = models.IntegerField(null=True)
    timer = models.IntegerField(null=True)  # in seconds
    deleted = models.BooleanField(default=False)
    version = models.IntegerField(default=0)
    def __str__(self):
        return '%s' % (self.title)


class Course(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    image = models.ImageField(upload_to='courses/', blank=True, null=True, verbose_name='Изображение')
    questions = models.ManyToManyField(Question, blank=True)
    questions_number = models.IntegerField()
    attempts = models.IntegerField(null=True)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                  through='UserCourseRelation', related_name='user')  # unusual relation table
    perfect_mark = models.IntegerField(null=True)  # percentage
    good_mark = models.IntegerField(null=True)
    satisfactory_mark = models.IntegerField(null=True)
    version = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)


    def __str__(self):
        return '%s' % (self.name)


class Answer(models.Model):
    # setting null to prevent auto deletion when question is deleted (we have 'deleted' field)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    text = models.TextField(blank=True, null=True)
    correct = models.BooleanField(default=False)
    weight = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='answers/', null=True, verbose_name='Изображение')
    audio = models.FileField(upload_to='answers_audio/', null=True)
    hint = models.CharField(max_length=255, null=True)
    priority = models.IntegerField(blank = True, null=True)
    deleted = models.BooleanField(default = False)

# intermediate models doc:
# https://docs.djangoproject.com/en/1.7/topics/db/models/#extra-fields-on-many-to-many-relationships

class UserCourseRelation(models.Model):  # relation-table with extra fields
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, )  # implicit link to django user
    course = models.ForeignKey(Course, on_delete=models.CASCADE, )  # implicit link to django user
    access = models.IntegerField(blank=True)  # 0 - user, 1 - manager
