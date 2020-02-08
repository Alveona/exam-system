from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from model_utils import Choices
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name = 'Profile_User')
    # related name supposed to prevent some clashes between two models, more here:
    # https://stackoverflow.com/questions/22538563/django-reverse-accessors-for-foreign-keys-clashing
    name = models.CharField(max_length = 255, null = True)
    surname = models.CharField(max_length = 255, null = True)
    activity = models.CharField(max_length=255, null=True)  # job or university
    image = models.ImageField(upload_to='users/', null=True)
    phone = models.CharField(max_length=16, null=True)
    ACCESS = ((0, 'student'), (1, 'teacher'), (2, 'admin'))
    group = models.IntegerField(choices=ACCESS, default=0)
    #username = models.CharField(max_length=255, default='')  # is meant to be empty
    #password = models.CharField(max_length=255, default='')  # is meant to be empty
