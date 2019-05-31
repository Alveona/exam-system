from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from exam_manage.models import Question, Course, Answer, StrictMode

class CourseSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    attempt_number = models.IntegerField(null=True)  # attempts of current course
    mode = models.ForeignKey(StrictMode, on_delete=models.CASCADE, null=True)
    finished = models.BooleanField(default=False)  # 1 is for finished


class SessionQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    session = models.ForeignKey(CourseSession, on_delete=models.CASCADE, null=True)
    order_number = models.IntegerField(null=True)
    result = models.IntegerField(null=True)
    attempts_number = models.IntegerField(null=True)  # attempts of current question
    finished = models.BooleanField(default=False)  # 1 is for finished

    def __str__(self):
        return '%s' % (self.question)


class SessionAnswer(models.Model):  # erased after question finished (i.e. written smth in SessionQuestion.Result)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    sessionQuestion = models.ForeignKey(SessionQuestion, on_delete=models.CASCADE, null=True)
    blocked = models.BooleanField(default=False)
    current_result = models.IntegerField(null = True)
    will_send_hint = models.BooleanField(default=False)
