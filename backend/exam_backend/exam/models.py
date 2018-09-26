from django.db import models
from django.conf import settings


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, null=True)
    text = models.TextField(null=True)
    answer_type = models.IntegerField(null=True, verbose_name='Тип вопроса')
    # answer_type: 1 - textbox / 2 - radio / 3 - checkbox
    image = models.ImageField(upload_to='images/', null=True, verbose_name='Изображение')
    # audio = <...>.AudioField (https://github.com/areski/django-audiofield)
    difficulty = models.IntegerField(null=True, verbose_name='Сложность')
    comment = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '%s' % (self.title)


class Course(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Изображение')
    questions = models.ManyToManyField(Question, blank=True)
    questions_number = models.IntegerField(null=True)  # зачем это нужно?
    # вместо UserCourse юзаем many-to-many с дополнительным классом информации о юзере
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Relation')

    def __str__(self):
        return '%s' % (self.name)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    text = models.TextField(blank=True, null=True)
    correct = models.BooleanField(default=False)
    weight = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', null=True, verbose_name='Изображение')

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

class Relation(models.Model):  # дополнительный класс для определения отношений, т.к. мы не юзаем relation-tables
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, )  # явное указание связи с джанго-юзером
    course = models.ForeignKey(Course, on_delete=models.CASCADE, )  # явное указание связи с курсом
    access = models.IntegerField(blank=True)  # 0 - user, 1 - manager
