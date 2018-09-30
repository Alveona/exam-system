from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Question, Answer, Course
from .serializers import QuestionSerializer, AnswerSerializer, CourseSerializer, \
    QuestionListSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()

    serializer_class = QuestionSerializer
    #serializer = QuestionSerializer()
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post', 'put']

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Question.objects.all().filter(id = self.request.query_params.get('id'),
                                                     user = self.request.user)
            return queryset
        if self.request.method == "DELETE":
            Answer.objects.all().filter(question = self.request.query_params.get('id'),
                                        user = self.request.user).delete()
            Question.objects.all().filter(id = self.request.query_params.get('id'),
                                          user = self.request.user).delete()
        user = self.request.user
        if user.is_superuser:
            queryset = Question.objects.all()
            return queryset
        return Question.objects.all().filter(user=user)

class QuestionListViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = Question.objects.all()
            return queryset
        return Question.objects.all().filter(user=user)

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post', 'put', 'delete', ]

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Answer.objects.all().filter(question = self.request.query_params.get('id'),
                                                     question__user = self.request.user)
            return queryset
        if self.request.method == "DELETE":
            print('object deleted')
        user = self.request.user
        if user.is_superuser:
            queryset = Answer.objects.all()
            return queryset
        return Answer.objects.all().filter(question__user=user)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post', 'put']