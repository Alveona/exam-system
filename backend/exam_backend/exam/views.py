from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Question, Answer, Course
from .serializers import QuestionSerializer, AnswerSerializer, CourseSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    #serializer = QuestionSerializer()
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post', 'put']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = Question.objects.all()
            return queryset
        return Question.objects.all().filter(user=user)