from django.test import TestCase
from django.conf import settings
#from django.core.management import setup_environ
#from exam import settings
#setup_environ(settings)
settings.configure()
from models import Course

def checkToken(token):
    token = Course.objects.all().filter(token = token)
    print(token.first())
    if(token.first()):
        print('token found')
    else:
        print('token not found')

checkToken('test42')
checkToken('test_kse')
