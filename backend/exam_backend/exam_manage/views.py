from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from .models import Question, Answer, Course, UserCourseRelation
from .serializers import QuestionSerializer, AnswerSerializer, CourseSerializer, \
    QuestionListSerializer, CourseCreatedSerializer, RelationSerializer, RelationUnsubscribeSerializer, \
    AnswerFormDataSerializer

class QuestionListViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = Question.objects.all()
            return queryset
        return Question.objects.all().filter(user=user)


class AnswerFormDataViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerFormDataSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', 'patch', 'get']

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Answer.objects.all().filter(question=self.request.query_params.get('id'),
                                                   question__user=self.request.user, deleted = False)
            return queryset
        # if self.request.method == "DELETE": # what was going on here?
            # print('object deleted')
        user = self.request.user
        if user.is_superuser:
            queryset = Answer.objects.all().filter(deleted = False)
            return queryset
        return Answer.objects.all().filter(question__user=user, deleted = False)

    def create(self, request, *args, **kwargs):
        # here we parse all answers came after the question
        # we use form-data as there are files to upload
        # TODO: look at https://www.django-rest-framework.org/api-guide/parsers/#formparser
        _dict = dict(self.request.data)
        print(_dict)
        question_to_parse = []
        text_to_parse = []
        correct_to_parse = []
        weight_to_parse = []
        audio_to_parse = []
        hint_to_parse = []
        priority_to_parse = []
        image_to_parse = []
        for value in _dict['question']:
            question_to_parse.append(value)
        for value in _dict['text']:
            text_to_parse.append(value)
        for value in _dict['correct']:
            correct_to_parse.append(value.capitalize())
        for value in _dict['weight']:
            weight_to_parse.append(value)
        for value in _dict['audio']:
            audio_to_parse.append(value if value != 'null' else None)
        print(audio_to_parse)
        for value in _dict['hint']:
            hint_to_parse.append(value if value != 'null' else None)
        for value in _dict['image']:
            image_to_parse.append(value if value != 'null' else None)
        for value in _dict['priority']:
            priority_to_parse.append(value)
        print('len: ' + str(len(question_to_parse)))

        successfully_created_answers = [] # used to easily revert all creates if exception occured
        try:
            for i in range(0, len(question_to_parse)):
                question = Question.objects.all().get(id=question_to_parse[i])
                answer = Answer(question=question, text=text_to_parse[i],
                                correct=correct_to_parse[i], weight=weight_to_parse[i],
                                audio=audio_to_parse[i], hint=hint_to_parse[i],
                                priority=priority_to_parse[i], image=image_to_parse[i], deleted = False)
                answer.save()
                successfully_created_answers.append(answer)
            return Response(status=status.HTTP_201_CREATED)
        except:
            # yup, we don't set 'deleted' to them, but directly delete from database because
            # something went completely wrong so we don't need partically written answers
            print('Unable to create object, clearing all them up')
            for ans in successfully_created_answers:
                ans.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()

    serializer_class = QuestionSerializer
    # serializer = QuestionSerializer()
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete', 'patch']
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if self.request.method == "GET":
            queryset = Question.objects.all().filter(id=self.request.query_params.get('id'),
                                                     user=user)
            return queryset
        if user.is_superuser: # TODO: either do this for all get's or delete it from here, no more methods support this logic
            queryset = Question.objects.all()
            return queryset
        return Question.objects.all().filter(user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.method == "DELETE":
            print('del')
            # if it is delete request, then mark answer as 'deleted' and delete only question
            answers = Answer.objects.all().filter(question=instance.id)
            for ans in answers:
                ans.deleted = True
                ans.save()
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            Answer.objects.all().filter(question=instance.id).delete()
        # otherwise delete question with constraints
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        validated_data = self.request.data
        question = self.get_object()
        answers = Answer.objects.all().filter(question = question)
        answers.delete() # we assume that there will be new answers after question

        question.title = validated_data['title']
        question.text = validated_data['text']
        question. answer_type = validated_data['answer_type']
        # question = Question(user=self.context['request'].user, title=validated_data['title'],
        #                     text=validated_data['text'], answer_type=validated_data['answer_type'])
        if 'timer' in validated_data:
            question.timer = validated_data['timer']
        if 'attempts_number' in validated_data:
            if question.attemtps_number is None or question.attempts_number <= validated_data['attempts_number']:
                question.attempts_number = validated_data['attempts_number']
        if 'answers_number' in validated_data:
            question.answers_number = validated_data['answers_number']
        if 'difficulty' in validated_data:
            question.difficulty = validated_data['difficulty']
        if 'comment' in validated_data:
            question.comment = validated_data['comment']
        if 'image' in validated_data:
            question.image = validated_data['image']
        if 'audio' in validated_data:
            question.audio = validated_data['audio']
        question.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()





class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete', 'patch']

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Answer.objects.all().filter(question=self.request.query_params.get('id'),
                                                   question__user=self.request.user, deleted = False)
            return queryset
        # if self.request.method == "DELETE":
            # print('object deleted')
        user = self.request.user
        if user.is_superuser:
            queryset = Answer.objects.all().filter(deleted = False)
            return queryset
        return Answer.objects.all().filter(question__user=user, deleted = False)

    def create(self, request, *args, **kwargs):
        print(self.request.data)
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    lookup_field = 'token' # used to allow delete on /api/courses/<token>/
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Course.objects.all().filter(token=self.request.query_params.get('token'))
            return queryset
        return Course.objects.all()

    def destroy(self, request, *args, **kwargs):
        # if self.request.method == "DELETE":
        instance = self.get_object()
        UserCourseRelation.objects.all().filter(course=instance).delete()
        CourseSession.objects.all().filter(course=instance).delete()
        Course.objects.all().get(token=instance.token).delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class CourseCreatedViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseCreatedSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Course.objects.all().filter(user=self.request.user).distinct()
            # print(queryset)
            if not queryset:
                return queryset
            for course in queryset:
                queryset_access = UserCourseRelation.objects.all().filter(course=course,
                                                                          user=self.request.user, access=1)
                # print(queryset_access)
                if not queryset_access:
                    queryset = queryset.exclude(id=course.id)
            return queryset


class CourseAddedViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseCreatedSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Course.objects.all().filter(user=self.request.user).distinct()
            # print(queryset)
            ids = []
            if not queryset:
                return queryset
            for course in queryset:
                queryset_access = UserCourseRelation.objects.all().filter(access=0, course=course,
                                                                          user=self.request.user)
                # print(queryset_access)
                if not queryset_access:
                    queryset = queryset.exclude(id=course.id)
            return queryset


class RelationViewSet(viewsets.ModelViewSet):
    queryset = UserCourseRelation.objects.all()
    serializer_class = RelationSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']

    # lookup_field = 'token'

    def get_queryset(self):
        return None


class RelationUnsubscribeViewSet(viewsets.ModelViewSet):
    queryset = UserCourseRelation.objects.all()
    serializer_class = RelationUnsubscribeSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        course = Course.objects.all().get(token=self.request.data['token'])
        relation = UserCourseRelation(user=self.request.user,
                                      course=course, access=0)
        relation.delete()
        return Response({'status': 'Successfully deleted'})
