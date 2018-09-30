from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=255, null = True) # job or university
    image = models.ImageField(upload_to='users/', null=True)
    phone = models.CharField(max_length=16, null=True)
    group = models.CharField(max_length=255, null=True)

    #class Meta:
        #db_table = 'auth_user'

class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, null=True)
    text = models.TextField(null=True)
    answer_type = models.IntegerField(null=True, verbose_name='Тип вопроса')
    # answer_type: 1 - textbox / 2 - radio / 3 - checkbox
    image = models.ImageField(upload_to='questions/', null=True, verbose_name='Изображение')
    # audio = <...>.AudioField (https://github.com/areski/django-audiofield)
    difficulty = models.IntegerField(null=True, verbose_name='Сложность')
    comment = models.CharField(max_length=255, blank=True)
    answers_number = models.IntegerField(null = True)
    audio = models.FileField(upload_to='questions_audio/', null = True)

    def __str__(self):
        return '%s' % (self.title)


class Course(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='courses/', blank=True, null=True, verbose_name='Изображение')
    questions = models.ManyToManyField(Question, blank=True)
    questions_number = models.IntegerField(null=True)  # зачем это нужно?
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UserCourseRelation') # нестандартная таблица отношений

    def __str__(self):
        return '%s' % (self.name)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    text = models.TextField(blank=True, null=True)
    correct = models.BooleanField(default=False)
    weight = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='answers/', null=True, verbose_name='Изображение')
    audio = models.FileField(upload_to='answers_audio/', null = True)
    hint = models.CharField(max_length=255, null = True)
    priority = models.IntegerField(null = True)

    def __str__(self):
        return '%s' % (self.text)


class CourseSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    attempt_number = models.IntegerField(null=True)  # attempts of current course
    finished = models.BooleanField(default=False)  # 1 is for finished


class SessionQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    session = models.ForeignKey(CourseSession, on_delete=models.CASCADE, null=True)
    orderNumber = models.IntegerField(null=True)
    result = models.IntegerField(null=True)
    attempt_number = models.IntegerField(null=True)  # attempts of current answer
    finished = models.BooleanField(default=False)  # 1 is for finished


class SessionAnswer(models.Model):  # erased after question finished (i.e. written smth in SessionQuestion.Result
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    sessionQuestion = models.ForeignKey(SessionQuestion, on_delete=models.CASCADE, null=True)


# док по intermediate models:
# https://docs.djangoproject.com/en/1.7/topics/db/models/#extra-fields-on-many-to-many-relationships

class UserCourseRelation(models.Model):  # relation-table с доп. параметрами
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, )  # явное указание связи с джанго-юзером
    course = models.ForeignKey(Course, on_delete=models.CASCADE, )  # явное указание связи с курсом
    access = models.IntegerField(blank=True)  # 0 - user, 1 - manager
