from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
import secrets, random
from rest_framework.decorators import action
from .models import Question, Answer, Course, Profile, UserCourseRelation, CourseSession, SessionAnswer, SessionQuestion
from .serializers import QuestionSerializer, AnswerSerializer, CourseSerializer, \
    QuestionListSerializer, ProfileSerializer, CourseCreatedSerializer, RelationSerializer, \
    SessionSerializer, SessionQuestionSerializer, SessionAnswerSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'patch', 'delete']

    def get_queryset(self):
        user = self.request.user
        if self.request.method == "GET":
            queryset = Profile.objects.all().filter(user=user)
            return queryset


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['post']


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
        if user.is_superuser:
            queryset = Question.objects.all()
            return queryset
        return Question.objects.all().filter(user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        Answer.objects.all().filter(question=instance.id).delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


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


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete', 'patch']

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Answer.objects.all().filter(question=self.request.query_params.get('id'),
                                                   question__user=self.request.user)
            return queryset
        if self.request.method == "DELETE":
            print('object deleted')
        user = self.request.user
        if user.is_superuser:
            queryset = Answer.objects.all()
            return queryset
        return Answer.objects.all().filter(question__user=user)

    def create(self, request, *args, **kwargs):
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
    lookup_field = 'token'
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Course.objects.all().filter(token=self.request.query_params.get('token'))
            return queryset
        return Course.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print('deleting course')
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

    def get_queryset(self):
        return None


class SessionViewSet(viewsets.ModelViewSet):
    queryset = CourseSession.objects.all()
    serializer_class = SessionSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']


class SessionQuestionViewSet(viewsets.ModelViewSet):
    queryset = SessionQuestion.objects.all()
    serializer_class = SessionQuestionSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get_queryset(self):
        session = CourseSession.objects.all().get(user=self.request.user, course__token=
                            self.request.query_params.get('token'), finished=False)
        print(session)
        question = SessionQuestion.objects.all().filter(session=session, finished=False)
        if not question:
            print("No unfinished sessions")
            current_question = max([session.order_number for session in SessionQuestion.objects.all().filter(session = session, finished = True)])

            if current_question >= session.course.questions_number:
                session.finished = True
                queryset = SessionQuestion.objects.none()
                print('test finished!')
                return queryset
                #raise serializers.ValidationError({'status': 'test is over'})
            # TODO DIFFICULTY FUNCTION
            course = Course.objects.all().get(token=self.request.query_params.get('token'))
            list_of_questions = course.questions.all()
            print(list_of_questions)
            question = secrets.choice(list_of_questions)
            print('chosen question is ' + str(question))
            previous_session_questions = SessionQuestion.objects.all().filter(session=session, finished=True)
            found_suitable_question = False
            while not found_suitable_question:
                for sq in previous_session_questions:
                    if question == sq.question:
                        question = secrets.choice(list_of_questions)
                        break
                    else:
                        found_suitable_question = True
                        print('chosen question in for is '+ str(question))
                        break
                continue
            session_q = SessionQuestion(question=question,
                                        session=session, order_number=current_question + 1,
                                        result=0, attempts_number=question.attempts_number,
                                        finished=False)
            print('s_q: ', end='')
            print(session_q)
            session_q.save()

            list_of_all_answers = Answer.objects.all().filter(question=question)
            print('list of all answers: ', end='')
            print(list_of_all_answers)
            list_of_answers = random.sample(set(list_of_all_answers), question.answers_number)
            print('list of answers: ', end='')
            print(list_of_answers)
            for answer in list_of_answers:
                session_a = SessionAnswer(sessionQuestion=session_q, blocked=False, answer=answer,
                                          current_result=answer.weight)
                session_a.save()
                print('s_a created: ', end='')
                print(session_a)
            print('s_q created:', end='')
            print(session_q)
            return SessionQuestion.objects.all().filter(id = session_q.id)
        print(question)
        return question


class SessionAnswerViewSet(viewsets.ModelViewSet):
    queryset = SessionAnswer.objects.all()
    serializer_class = SessionAnswerSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        print(self.request.data)
        question = SessionQuestion.objects.all().get(id=self.request.data['id'])
        answers_list = self.request.data['answers']
        print(answers_list)
        print('answer_type: ', end='')
        print(question.question.answer_type)
        answers_of_question = SessionAnswer.objects.all().filter(sessionQuestion=question, blocked=False)
        if question.question.answer_type == 1:
            #print(SessionQuestion.objects.all())
            print(SessionAnswer.objects.all().get(sessionQuestion=question))
            correct_answer = SessionAnswer.objects.all().get(sessionQuestion=question)
            print('correct answer is ', end='')
            print(correct_answer.answer.text)
            print('your answer is ', end='')
            print(answers_list[0])
            if answers_list[0] == correct_answer.answer.text:
                print('your answer is correct')
                correct_answer.blocked = True
                correct_answer.save()
                question.result += correct_answer.current_result
                question.finished = True
                question.save()
                correct_answer.delete()
                return Response({'status': 'all ok'})
            else:
                print('your answer is incorrect')
                print('previous number of attempts is ', end='')
                print(question.attempts_number)
                #print(correct_answer.current_result)
                question.attempts_number = question.attempts_number - 1
                if question.attempts_number == 0:
                    question.result = 0  # TODO IF ANSWER_TYPE == 2 || 3, COLLECT RESULT FROM S_ANSWERS
                    question.finished = True
                    question.save()
                    correct_answer.delete()
                    return Response({'status': 'attempts are over'})
                print('current number of attempts is ', end='')
                print(question.attempts_number)
                question.save()
                print('current result before division: ', end='')
                print(correct_answer.current_result)
                correct_answer.current_result = correct_answer.current_result / 2
                correct_answer.save()
                if correct_answer.current_result == 0:
                    question.result = 0
                    question.finished = True
                    question.save()
                    correct_answer.delete()
                print('current result is', end='')
                print(correct_answer.current_result)
                return Response({'status': 'something is wrong'})

    def get_queryset(self):
        question = SessionQuestion.objects.all().get(id=self.request.query_params.get('id'))
        answers = SessionAnswer.objects.all().filter(sessionQuestion=question)
        return answers
