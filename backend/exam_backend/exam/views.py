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
    SessionSerializer, SessionQuestionSerializer, SessionAnswerSerializer, RelationUnsubscribeSerializer


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
    #lookup_field = 'token'

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


class SessionViewSet(viewsets.ModelViewSet):
    queryset = CourseSession.objects.all()
    serializer_class = SessionSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']
    ''' def get_queryset(self):
        if self.request.method == 'GET':
            session = CourseSession.objects.all().filter(course__token = self.request.query_params.get('token'), finished = True)
            #sessions_q = 
        return self.queryset'''


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

            list_of_correct_answers = list(Answer.objects.all().filter(question=question, correct=True))
            print('correct list: ' + str(list_of_correct_answers))
            list_of_incorrect_answers = list(Answer.objects.all().filter(question=question, correct=False))
            print('incorrect list: ' + str(list_of_incorrect_answers))
            list_of_answers = list_of_correct_answers
            list_of_answers += random.sample(set(list_of_incorrect_answers),
                                             question.answers_number - len(list_of_correct_answers))
            random.shuffle(list_of_answers)
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
    #answer_to_hint = None

    def create(self, request, *args, **kwargs):
        question = SessionQuestion.objects.all().get(id=self.request.data['id'])

        if self.request.data['status'] == 2:
            answers = SessionAnswer.objects.all().filter(sessionQuestion=question)
            question.result = 0
            question.finished = True
            question.save()
            answers.delete()
        if self.request.data['status'] == 3:
            question.result = 0
            question.finished = True
            question.save()
            course = Course.objects.all().get(token=self.request.query_params.get('token'))
            session = CourseSession.objects.all().get(user=self.request.user, course__token=
                                        self.request.query_params.get('token'), finished=False)
            current_question = max([session.order_number for session in
                                    SessionQuestion.objects.all().filter(session=session, finished=True)])
            list_of_questions = course.questions.all()
            question = secrets.choice(list_of_questions)
            previous_session_questions = SessionQuestion.objects.all().filter(session=session, finished=True)
            found_suitable_question = False
            while not found_suitable_question:
                for sq in previous_session_questions:
                    if question == sq.question:
                        question = secrets.choice(list_of_questions)
                        break
                    else:
                        found_suitable_question = True
                        break
                continue
            session_q = SessionQuestion(question=question,
                                        session=session, order_number=current_question + 1,
                                        result=0, attempts_number=question.attempts_number,
                                        finished=True)
            session_q.save()


        if question.question.answer_type == 1:
            print(self.request.data)

            answers_list = self.request.data['answers']
            print(answers_list)
            print('answer_type: ', end='')
            print(question.question.answer_type)
            print(SessionAnswer.objects.all().get(sessionQuestion=question))
            correct_answer = SessionAnswer.objects.all().get(sessionQuestion=question)
            correct_answer.will_send_hint = False
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
                    question.result = 0
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
                #self.answer_to_hint = correct_answer
                correct_answer.will_send_hint = True
                return Response({'status': 'something is wrong'})

        if question.question.answer_type == 2:
            print(self.request.data)
            answers_list = self.request.data['answers']
            print(answers_list)
            ids = []
            chosen = []
            for object in answers_list:
                ids.append(object['id'])
                chosen.append(object['chosen'])

            answers_dict = dict(zip(ids, chosen))
            print('answers_dict: ' + str(answers_dict))
            print('answer_type: ', end='')
            #print(question)
            print(question.question.answer_type)
            print(SessionAnswer.objects.all().filter(sessionQuestion=question))
            correct_answer = SessionAnswer.objects.all().get(sessionQuestion=question, answer__correct = True)
            print('correct answer is ', end='')
            print(correct_answer.answer.id)

            answers = SessionAnswer.objects.all().filter(sessionQuestion = question).order_by('answer__priority')
            for answer in answers:
                answer.will_send_hint = False
                print(str(answer) + ' prior: ' + str(answer.answer.priority) + ' correct: ' + str(answer.answer.correct))

            intermediate_correct = 0
            should_be_correct = question.question.answers_number
            for _id, chosen in answers_dict.items():
                for answer in answers:
                    if answer.id == _id:
                        if answer.answer.correct == chosen:
                            intermediate_correct+=1
                            print(intermediate_correct)

            if intermediate_correct == should_be_correct:
                for answer in answers:
                    question.result += answer.current_result
                    question.finished = True
                    question.save()
                    answers.delete()
                    return Response({'status': 'all ok'})
            else:
                print(intermediate_correct)
                print('question ' + str(answers.filter(answer__priority = intermediate_correct + 1)) +' failed')
                print('your answer is incorrect')
                print('previous number of attempts is ', end='')
                print(question.attempts_number)
                # print(correct_answer.current_result)
                question.attempts_number = question.attempts_number - 1
                if question.attempts_number == 0:
                    question.result = 0
                    question.finished = True
                    question.save()
                    answers.delete()
                    return Response({'status': 'attempts are over'})
                print('current number of attempts is ', end='')
                print(question.attempts_number)
                question.save()
                for answer in answers:
                    answer.current_result = answer.current_result / 2
                    print('current result of answer is ' + str(answer.current_result))
                    answer.save()

                result_sum = 0
                for answer in answers:
                    result_sum += answer.current_result
                if result_sum == 0:
                    question.result = 0
                    question.finished = True
                    question.save()
                    answers.delete()
                    return Response({'status': 'all results are zero'})

                answers.get(answer__priority = intermediate_correct + 1).will_send_hint = True
                return Response({'status': 'something is wrong'})

        if question.question.answer_type == 3:
            print(self.request.data)
            answers_list = self.request.data['answers']
            print(answers_list)
            ids = []
            chosen = []
            for object in answers_list:
                ids.append(object['id'])
                chosen.append(object['chosen'])

            answers_dict = dict(zip(ids, chosen))
            print('answers_dict: ' + str(answers_dict))
            print('answer_type: ', end='')
            #print(question)
            print(question.question.answer_type)
            print(SessionAnswer.objects.all().filter(sessionQuestion=question))
            correct_answer = SessionAnswer.objects.all().get(sessionQuestion=question, answer__correct = True)
            print('correct answer is ', end='')
            print(correct_answer.answer.id)

            answers = SessionAnswer.objects.all().filter(sessionQuestion = question).order_by('answer__priority')
            for answer in answers:
                answer.will_send_hint = False
                print(str(answer) + ' prior: ' + str(answer.answer.priority) + ' correct: ' + str(answer.answer.correct))

            intermediate_correct = 0
            should_be_correct = question.question.answers_number
            incorrect_chosen = 0
            correct_not_chosen = 0
            for _id, chosen in answers_dict.items():
                for answer in answers:
                    if answer.id == _id:
                        if answer.answer.correct == chosen:
                            intermediate_correct+=1
                            print(intermediate_correct)
                        else:
                            if answer.answer.correct == False:
                                incorrect_chosen += 1
                            else:
                                correct_not_chosen += 1

            if intermediate_correct == should_be_correct:
                for answer in answers:
                    question.result += answer.current_result
                    question.finished = True
                    question.save()
                    answers.delete()
                    return Response({'status': 'all ok'})
            else:
                if incorrect_chosen > 0:
                    print(intermediate_correct)
                    print('question ' + str(answers.filter(answer__priority = intermediate_correct + 1)) +' failed')
                    print('your answer is incorrect')
                    print('previous number of attempts is ', end='')
                    print(question.attempts_number)
                    # print(correct_answer.current_result)
                    question.attempts_number = question.attempts_number - 1
                    if question.attempts_number == 0:
                        for answer in answers:
                            question.result += answer.result
                        question.finished = True
                        question.save()
                        answers.delete()
                        return Response({'status': 'attempts are over'})
                    print('current number of attempts is ', end='')
                    print(question.attempts_number)
                    question.save()
                    for answer in answers:
                        if answer.blocked == False:
                            answer.current_result = answer.current_result / 2
                        print('current result of answer is ' + str(answer.current_result))
                        answer.save()

                    result_sum = 0
                    for answer in answers:
                        result_sum += answer.current_result
                    if result_sum == 0:
                        question.result = 0
                        question.finished = True
                        question.save()
                        answers.delete()
                        return Response({'status': 'all results are zero'})

                    answers.get(answer__priority = intermediate_correct + 1).will_send_hint = True
                    return Response({'status': 'incorrect chosen'})
                else:
                    print(intermediate_correct)
                    print('question ' + str(answers.filter(answer__priority=intermediate_correct + 1)) + ' failed')
                    print('your answer is incorrect')
                    print('previous number of attempts is ', end='')
                    print(question.attempts_number)
                    # print(correct_answer.current_result)
                    question.attempts_number = question.attempts_number - 1
                    if question.attempts_number == 0:
                        for answer in answers:
                            question.result += answer.result
                        question.finished = True
                        question.save()
                        answers.delete()
                        return Response({'status': 'attempts are over'})
                    print('current number of attempts is ', end='')
                    print(question.attempts_number)
                    question.save()
                    for i in range(1, intermediate_correct):
                        answer = answers.get(answer__priority = i, answer__correct = True)
                        if answer:
                            answer.blocked = True

                    for answer in answers:
                        if answer.blocked == False:
                            answer.current_result = answer.current_result / 2
                        print('current result of answer is ' + str(answer.current_result))
                        answer.save()

                    result_sum = 0
                    for answer in answers:
                        result_sum += answer.current_result
                    if result_sum == 0:
                        question.result = 0
                        question.finished = True
                        question.save()
                        answers.delete()
                        return Response({'status': 'all results are zero'})

                    answers.get(answer__priority=intermediate_correct + 1).will_send_hint = True
                    return Response({'status': 'not all corrects chosen'})


    def get_queryset(self):
        question = SessionQuestion.objects.all().get(id=self.request.query_params.get('id'))
        answers = SessionAnswer.objects.all().filter(sessionQuestion=question)
        return answers
