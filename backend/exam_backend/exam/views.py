from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Question, Answer, Course, Profile, UserCourseRelation
from .serializers import QuestionSerializer, AnswerSerializer, CourseSerializer, \
    QuestionListSerializer, ProfileSerializer, CourseCreatedSerializer, RelationSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'patch', 'delete']
    def get_queryset(self):
        user = self.request.user
        if self.request.method == "GET":
            queryset = Profile.objects.all().filter(user = user)
            return queryset

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['post']

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()

    serializer_class = QuestionSerializer
    #serializer = QuestionSerializer()
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post', 'put', 'delete', 'patch']
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if self.request.method == "GET":
            queryset = Question.objects.all().filter(id = self.request.query_params.get('id'),
                                                     user = user)
            return queryset
        if user.is_superuser:
            queryset = Question.objects.all()
            return queryset
        return Question.objects.all().filter(user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        Answer.objects.all().filter(question = instance.id).delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


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
    http_method_names = ['get', 'post', 'put', 'delete', 'patch']

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Course.objects.all().filter(token = self.request.query_params.get('token'))
            return queryset

class CourseCreatedViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseCreatedSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get']

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Course.objects.all().filter(user = self.request.user).distinct()
            #print(queryset)
            if not queryset:
                return queryset
            for course in queryset:
                queryset_access = UserCourseRelation.objects.all().filter(course = course,
                                                                          user = self.request.user, access = 1)
                #print(queryset_access)
                if not queryset_access:
                    queryset = queryset.exclude(id = course.id)
            return queryset


class CourseAddedViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseCreatedSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Course.objects.all().filter(user=self.request.user).distinct()
            #print(queryset)
            ids = []
            if not queryset:
                return queryset
            for course in queryset:
                queryset_access = UserCourseRelation.objects.all().filter(access = 0, course=course,
                                                                          user=self.request.user)
                #print(queryset_access)
                if not queryset_access:
                    queryset = queryset.exclude(id = course.id)
            return queryset


class RelationViewSet(viewsets.ModelViewSet):
    queryset = UserCourseRelation.objects.all()
    serializer_class = RelationSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['post']

    def get_queryset(self):
        return None
