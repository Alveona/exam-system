from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
import secrets, random
from rest_framework.decorators import action
from .models import CourseSession, SessionAnswer, SessionQuestion
from .serializers import (
    SessionSerializer,
    SessionQuestionSerializer,
    SessionAnswerSerializer,
    RelationUnsubscribeSerializer,
    SessionStatsSerializer,
    CourseTokenAjaxSerializer,
)
from exam_manage.models import Question, Answer, Course
import heapq


class SessionViewSet(viewsets.ModelViewSet):
    queryset = CourseSession.objects.all()
    serializer_class = SessionSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["post"]
    """ def get_queryset(self):
        if self.request.method == 'GET':
            session = CourseSession.objects.all().filter(course__token = self.request.query_params.get('token'), finished = True)
            #sessions_q =
        return self.queryset"""


class SessionStatsViewSet(viewsets.ModelViewSet):
    queryset = CourseSession.objects.all()
    serializer_class = SessionStatsSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]

    def get_queryset(self):
        if self.request.method == "GET":
            session = (
                CourseSession.objects.all()
                .filter(
                    course__user=self.request.user,
                    course__token=self.request.query_params.get("token"),
                )
                .order_by("-attempt_number")
                .first()
            )
            empty = CourseSession.objects.none()
            list = []
            list.append(session)
            return list
        return self.queryset


class SessionQuestionViewSet(viewsets.ModelViewSet):
    queryset = SessionQuestion.objects.all()
    serializer_class = SessionQuestionSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]

    def get_queryset(self):

        session = CourseSession.objects.all().get(
            user=self.request.user,
            course__token=self.request.query_params.get("token"),
            finished=False,
        )

        question = SessionQuestion.objects.all().filter(session=session, finished=False)
        if not question:

            try:
                current_question = max(
                    [
                        session.order_number
                        for session in SessionQuestion.objects.all().filter(
                            session=session, finished=True
                        )
                    ]
                )
            except:
                current_question = 1

            if current_question >= session.course.questions_number:
                session.finished = True
                session.save()
                queryset = SessionQuestion.objects.none()

                return queryset

            # TODO DIFFICULTY FUNCTION
            course = Course.objects.all().get(
                token=self.request.query_params.get("token")
            )
            list_of_questions = course.questions.all()

            question = secrets.choice(list_of_questions)

            previous_session_questions = SessionQuestion.objects.all().filter(
                session=session, finished=True
            )
            previous_questions = [
                sessionq.question for sessionq in previous_session_questions
            ]

            found_suitable_question = False
            while not found_suitable_question:

                if question in previous_questions:

                    list_of_questions = list_of_questions.exclude(id=question.id)
                    question = secrets.choice(list_of_questions)
                else:
                    found_suitable_question = True

            session_q = SessionQuestion(
                question=question,
                session=session,
                order_number=current_question + 1,
                result=0,
                attempts_number=question.attempts_number,
                finished=False,
            )

            session_q.save()

            list_of_correct_answers = list(
                Answer.objects.all().filter(
                    question=question, correct=True, deleted=False
                )
            )

            list_of_incorrect_answers = list(
                Answer.objects.all().filter(
                    question=question, correct=False, deleted=False
                )
            )

            list_of_answers = list_of_correct_answers
            list_of_answers += random.sample(
                set(list_of_incorrect_answers),
                question.answers_number - len(list_of_correct_answers),
            )
            random.shuffle(list_of_answers)

            for answer in list_of_answers:
                session_a = SessionAnswer(
                    sessionQuestion=session_q,
                    blocked=False,
                    answer=answer,
                    current_result=answer.weight,
                )
                session_a.save()

            return SessionQuestion.objects.all().filter(id=session_q.id)

        return question


class SessionAnswerViewSet(viewsets.ModelViewSet):
    queryset = SessionAnswer.objects.all()
    serializer_class = SessionAnswerSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post"]

    def create(self, request, *args, **kwargs):
        question = SessionQuestion.objects.all().get(id=self.request.data["id"])

        if self.request.data["status"] == 2:
            answers = SessionAnswer.objects.all().filter(
                sessionQuestion=question, answer__deleted=False
            )
            question.result = 0
            question.finished = True
            question.save()
            answers.delete()

            return Response({"status": "skiped"})
        if self.request.data["status"] == 3:

            question.result = 0
            question.finished = True
            question.save()

            course = question.session.course
            session = CourseSession.objects.all().get(
                user=self.request.user, course__token=course.token, finished=False
            )
            current_question = max(
                [
                    session.order_number
                    for session in SessionQuestion.objects.all().filter(
                        session=session, finished=True
                    )
                ]
            )
            for i in range(current_question, course.questions_number):
                current_question = max(
                    [
                        session.order_number
                        for session in SessionQuestion.objects.all().filter(
                            session=session, finished=True
                        )
                    ]
                )
                list_of_questions = course.questions.all()

                question = secrets.choice(list_of_questions)
                previous_session_questions = SessionQuestion.objects.all().filter(
                    session=session, finished=True
                )
                previous_questions = [
                    sessionq.question for sessionq in previous_session_questions
                ]

                found_suitable_question = False
                while not found_suitable_question:

                    if question in previous_questions:

                        list_of_questions = list_of_questions.exclude(id=question.id)
                        question = secrets.choice(list_of_questions)
                    else:
                        found_suitable_question = True

                session_q = SessionQuestion(
                    question=question,
                    session=session,
                    order_number=current_question + 1,
                    result=0,
                    attempts_number=question.attempts_number,
                    finished=True,
                )
                session_q.save()
                answers = SessionAnswer.objects.all().filter(
                    sessionQuestion=session_q, answer__deleted=False
                )
                answers.delete()

            return Response({"status": "aborted"})

        if question.question.answer_type == 1:

            answers_list = self.request.data["answers"]

            correct_answer = SessionAnswer.objects.all().get(
                sessionQuestion=question, answer__deleted=False
            )
            correct_answer.will_send_hint = False

            if len(answers_list) >= 1 and answers_list[0] == correct_answer.answer.text:

                correct_answer.blocked = True
                correct_answer.save()
                question.result += correct_answer.current_result
                question.finished = True
                question.save()
                correct_answer.delete()
                return Response({"status": "all ok"})
            else:

                if question.attempts_number:

                    question.attempts_number = question.attempts_number - 1
                    if question.attempts_number == 0:
                        question.result = 0
                        question.finished = True
                        question.save()
                        correct_answer.delete()
                        return Response({"status": "attempts are over"})

                    question.save()

                correct_answer.current_result = correct_answer.current_result // 2
                correct_answer.save()
                if correct_answer.current_result == 0:
                    question.result = 0
                    question.finished = True
                    question.save()
                    correct_answer.delete()

                correct_answer.will_send_hint = True
                correct_answer.save()
                return Response({"status": "something is wrong"})

        if question.question.answer_type == 2 or question.question.answer_type == 3:

            answers_list = self.request.data["answers"]

            ids = []
            chosen = []
            for object in answers_list:
                ids.append(object["id"])
                chosen.append(object["chosen"])

            answers_dict = dict(zip(ids, chosen))

            correct_answer = SessionAnswer.objects.all().filter(
                sessionQuestion=question, answer__correct=True, answer__deleted=False
            )

            answers = (
                SessionAnswer.objects.all()
                .filter(sessionQuestion=question, answer__deleted=False)
                .order_by("answer__priority")
            )
            for answer in answers:
                answer.will_send_hint = False
                answer.save()

            intermediate_correct_by_priority = 0
            intermediate_correct = 0
            should_be_correct = question.question.answers_number
            incorrect_chosen = 0
            correct_not_chosen = 0
            found_error = False
            for answer in answers:
                for _id, chosen in answers_dict.items():
                    if answer.id == _id:

                        if answer.answer.correct == chosen:

                            if found_error is False:
                                intermediate_correct_by_priority += 1
                            intermediate_correct += 1

                        else:

                            if answer.answer.correct == False:
                                incorrect_chosen += 1
                            else:
                                correct_not_chosen += 1
                            break
                else:  # https://stackoverflow.com/questions/653509/breaking-out-of-nested-loops

                    continue
                found_error = True
                continue

            if intermediate_correct_by_priority == should_be_correct:
                for answer in answers:
                    question.result += answer.current_result
                    question.finished = True
                    question.save()
                    answers.delete()
                return Response({"status": "all ok"})
            else:
                if incorrect_chosen > 0:

                    priority_list = []
                    for answer in answers:
                        priority_list.append(answer.answer.priority)

                    priority = heapq.nsmallest(
                        intermediate_correct_by_priority + 1, priority_list
                    )

                    if question.attempts_number:

                        question.attempts_number = question.attempts_number - 1
                        if question.attempts_number == 0:
                            for answer in answers:
                                question.result += answer.current_result
                            question.finished = True
                            question.save()
                            answers.delete()
                            return Response({"status": "attempts are over"})

                        question.save()
                    for answer in answers.filter(blocked=False):
                        if answer.blocked is False:
                            answer.current_result = answer.current_result // 2
                            answer.save()

                    result_sum = 0
                    blocked_sum = 0
                    for answer in answers.filter(blocked=True):
                        blocked_sum += answer.current_result

                    for answer in answers.filter(blocked=False):
                        result_sum += answer.current_result

                    if result_sum == 0:

                        question.result = blocked_sum
                        question.finished = True
                        question.save()
                        answers.delete()
                        return Response({"status": "all results are zero"})
                    priority = heapq.nsmallest(
                        intermediate_correct_by_priority + 1, priority_list
                    )
                    incor_ans = answers.get(answer__priority=priority[-1])
                    incor_ans.will_send_hint = True
                    incor_ans.save()
                    return Response({"status": "incorrect chosen"})
                else:

                    priority_list = []
                    for answer in answers:
                        priority_list.append(answer.answer.priority)

                    priority = heapq.nsmallest(
                        intermediate_correct_by_priority + 1, priority_list
                    )

                    if question.attempts_number:

                        question.attempts_number = question.attempts_number - 1
                        if question.attempts_number == 0:
                            for answer in answers:
                                question.result += answer.current_result
                            question.finished = True
                            question.save()
                            answers.delete()
                            return Response({"status": "attempts are over"})

                        question.save()
                    for i in range(1, len(answers_dict) + 1):

                        priority = heapq.nsmallest(i, priority_list)

                        answer = answers.filter(answer__priority=priority[-1])

                        if answer:
                            answer = answer.first()

                            if (
                                answers_dict[answer.id] is True
                                and answer.answer.correct is True
                            ):

                                answer.blocked = True
                                answer.save()

                                continue

                    for answer in answers.filter(blocked=False):

                        if answer.blocked is False:
                            answer.current_result = answer.current_result // 2
                            answer.save()

                        # answer.save()
                        # well, idk why but in case of unnecessary(extra) savings just in case, it drops
                        # some field's values to default, similar to described here
                        # https://code.djangoproject.com/ticket/27335?cversion=0&cnum_hist=3

                    result_sum = 0
                    blocked_sum = 0
                    for answer in answers.filter(blocked=True):
                        blocked_sum += answer.current_result

                    for answer in answers.filter(blocked=False):
                        result_sum += answer.current_result

                    if result_sum == 0:

                        question.result = blocked_sum
                        question.finished = True
                        question.save()
                        answers.delete()
                        return Response({"status": "all results are zero"})

                    priority = heapq.nsmallest(
                        intermediate_correct_by_priority + 1, priority_list
                    )
                    incor_ans = answers.get(answer__priority=priority[-1])
                    if incor_ans:
                        incor_ans.will_send_hint = True
                        incor_ans.save()
                    return Response({"status": "not all corrects chosen"})

    def get_queryset(self):
        question = SessionQuestion.objects.all().get(
            id=self.request.query_params.get("id")
        )
        if question:
            answers = SessionAnswer.objects.all().filter(
                sessionQuestion=question, answer__deleted=False
            )
            return answers
        return Answer.objects.none()


class CourseTokenAjaxViewset(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseTokenAjaxSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["post"]

    def isTokenAvaliable(self, token):
        token = Course.objects.all().filter(token=token)

        if token.first():

            return False
        else:

            return True

    def create(self, request, *args, **kwargs):
        token = self.request.data["token"]
        if self.isTokenAvaliable(token):
            return Response({"avaliable": "true"})  # TODO change to bool
        else:
            return Response({"avaliable": "false"})

