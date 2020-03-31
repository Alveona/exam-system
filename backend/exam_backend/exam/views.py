from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
import secrets, random
from rest_framework.decorators import action
from .models import CourseSession, SessionAnswer, SessionQuestion
from .serializers import SessionSerializer, SessionQuestionSerializer, SessionAnswerSerializer, RelationUnsubscribeSerializer, \
    SessionStatsSerializer, CourseTokenAjaxSerializer
from exam_manage.models import Question, Answer, Course
import heapq

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


class SessionStatsViewSet(viewsets.ModelViewSet):
    queryset = CourseSession.objects.all()
    serializer_class = SessionStatsSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get_queryset(self):
        if self.request.method == 'GET':
            session = CourseSession.objects.all().filter(course__user=self.request.user,
                                                         course__token=self.request.query_params.get('token')). \
                order_by('-attempt_number').first()
            empty = CourseSession.objects.none()
            list = []
            list.append(session)
            return list
        return self.queryset


class SessionQuestionViewSet(viewsets.ModelViewSet):
    queryset = SessionQuestion.objects.all()
    serializer_class = SessionQuestionSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get_queryset(self):
        print('GET on /session-q')
        session = CourseSession.objects.all().get(user=self.request.user, course__token=
        self.request.query_params.get('token'), finished=False)
        # print(session)
        question = SessionQuestion.objects.all().filter(session=session, finished=False)
        if not question:
            # print("No unfinished sessions")
            try:
                current_question = max([session.order_number for session in
                                    SessionQuestion.objects.all().filter(session=session, finished=True)])
            except:
                current_question = 1
            print(session.course.questions_number)
            if current_question >= session.course.questions_number:
                session.finished = True
                session.save()
                queryset = SessionQuestion.objects.none()
                # print('test finished!')
                return queryset
                # raise serializers.ValidationError({'status': 'test is over'})
            # TODO DIFFICULTY FUNCTION
            course = Course.objects.all().get(token=self.request.query_params.get('token'))
            list_of_questions = course.questions.all()
            print('list of questions: ' + str(list_of_questions))
            question = secrets.choice(list_of_questions)

            previous_session_questions = SessionQuestion.objects.all().filter(session=session, finished=True)
            previous_questions = [sessionq.question for sessionq in previous_session_questions]
            print('previous s-qs: ' + str(previous_session_questions))
            print('previous qs: ' + str(previous_questions))
            found_suitable_question = False
            while not found_suitable_question:
                print('current checking question is: ' + str(question))
                if question in previous_questions:
                    print('no, it is not suitable')
                    list_of_questions = list_of_questions.exclude(id = question.id)
                    question = secrets.choice(list_of_questions)
                else:
                    found_suitable_question = True
            # while not found_suitable_question:
            #     print('found suitable? ' + str(found_suitable_question))
            #     for sq in previous_session_questions:
            #         print('comparing ' + str(question) + ' and ' + str(sq.question))
            #         if question == sq.question:
            #             list_of_questions.exclude(id = question.id)
            #             question = secrets.choice(list_of_questions)
            #             break
            #         else:
            #             found_suitable_question = True
            #             # print('chosen question in for is '+ str(question))
            #             break
            #     continue
            print('chosen question is ' + str(question))
            session_q = SessionQuestion(question=question,
                                        session=session, order_number=current_question + 1,
                                        result=0, attempts_number=question.attempts_number,
                                        finished=False)
            # print('s_q: ', end='')
            # print(session_q)
            session_q.save()

            list_of_correct_answers = list(Answer.objects.all().filter(question=question, correct=True, deleted = False))
            # print('correct list: ' + str(list_of_correct_answers))
            list_of_incorrect_answers = list(Answer.objects.all().filter(question=question, correct=False, deleted = False))
            # print('incorrect list: ' + str(list_of_incorrect_answers))
            list_of_answers = list_of_correct_answers
            list_of_answers += random.sample(set(list_of_incorrect_answers),
                                             question.answers_number - len(list_of_correct_answers))
            random.shuffle(list_of_answers)
            # print('list of answers: ', end='')
            # print(list_of_answers)
            for answer in list_of_answers:
                session_a = SessionAnswer(sessionQuestion=session_q, blocked=False, answer=answer,
                                          current_result=answer.weight)
                session_a.save()
                print('s_a created: ', end='')
                print(session_a)
                print(' for answer ' + str(answer))
            # print('s_q created:', end='')
            # print(session_q)
            return SessionQuestion.objects.all().filter(id=session_q.id)
        # print(question)
        return question


class SessionAnswerViewSet(viewsets.ModelViewSet):
    queryset = SessionAnswer.objects.all()
    serializer_class = SessionAnswerSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        question = SessionQuestion.objects.all().get(id=self.request.data['id'])

        if self.request.data['status'] == 2:
            answers = SessionAnswer.objects.all().filter(sessionQuestion=question, answer__deleted = False)
            question.result = 0
            question.finished = True
            question.save()
            answers.delete()
            # answers.save()
            return Response({'status': 'skiped'})
        if self.request.data['status'] == 3:

            print(self.request.data)
            question.result = 0
            question.finished = True
            question.save()
            # course = Course.objects.all().get(token=self.request.query_params.get('token'))
            course = question.session.course
            session = CourseSession.objects.all().get(user=self.request.user, course__token=
            course.token, finished=False)
            current_question = max([session.order_number for session in
                                    SessionQuestion.objects.all().filter(session=session, finished=True)])
            for i in range(current_question, course.questions_number):
                current_question = max([session.order_number for session in
                                                    SessionQuestion.objects.all().filter(session=session, finished=True)])
                list_of_questions = course.questions.all()
                print(list_of_questions)
                question = secrets.choice(list_of_questions)
                previous_session_questions = SessionQuestion.objects.all().filter(session=session, finished=True)
                previous_questions = [sessionq.question for sessionq in previous_session_questions]

                print('previous s-qs: ' + str(previous_session_questions))
                print('previous qs: ' + str(previous_questions))
                found_suitable_question = False
                while not found_suitable_question:
                    print('current checking question is: ' + str(question))
                    if question in previous_questions:
                        print('no, it is not suitable')
                        list_of_questions = list_of_questions.exclude(id = question.id)
                        question = secrets.choice(list_of_questions)
                    else:
                        found_suitable_question = True
                print('chosen question is ' + str(question))
                session_q = SessionQuestion(question=question,
                                            session=session, order_number=current_question + 1,
                                            result=0, attempts_number=question.attempts_number,
                                            finished=True)
                session_q.save()
                answers = SessionAnswer.objects.all().filter(sessionQuestion=session_q, answer__deleted = False)
                answers.delete()
            # answers.save()
            print('going to abort')
            return Response({'status': 'aborted'})

        if question.question.answer_type == 1:
            print(self.request.data)
            answers_list = self.request.data['answers']
            print(answers_list)
            print('answer_type: ', end='')
            print(question.question.answer_type)
            print(SessionAnswer.objects.all().get(sessionQuestion=question, answer__deleted = False))
            correct_answer = SessionAnswer.objects.all().get(sessionQuestion=question, answer__deleted = False)
            correct_answer.will_send_hint = False
            print('correct answer is ', end='')
            print(correct_answer.answer.text)
            print('your answer is ', end='')
            print(answers_list[0] if len(answers_list) >= 1 else None)
            if len(answers_list) >= 1 and answers_list[0] == correct_answer.answer.text:
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

                # print(correct_answer.current_result)
                if question.attempts_number:
                    print('previous number of attempts is ', end='')
                    print(question.attempts_number)
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
                correct_answer.current_result = correct_answer.current_result // 2
                correct_answer.save()
                if correct_answer.current_result == 0:
                    question.result = 0
                    question.finished = True
                    question.save()
                    correct_answer.delete()
                print('current result is', end='')
                print(correct_answer.current_result)
                # self.answer_to_hint = correct_answer
                correct_answer.will_send_hint = True
                correct_answer.save()
                return Response({'status': 'something is wrong'})

        if question.question.answer_type == 2 or question.question.answer_type == 3:
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
            # print(question)
            print(question.question.answer_type)
            print(SessionAnswer.objects.all().filter(sessionQuestion=question, answer__deleted = False))
            correct_answer = SessionAnswer.objects.all().filter(sessionQuestion=question, answer__correct=True, answer__deleted = False)
            print('correct answer are ', end='')
            print(correct_answer)

            answers = SessionAnswer.objects.all().filter(sessionQuestion=question, answer__deleted = False).order_by('answer__priority')
            for answer in answers:
                answer.will_send_hint = False
                answer.save()
                print(
                    str(answer) + ' prior: ' + str(answer.answer.priority) + ' correct: ' + str(answer.answer.correct))

            intermediate_correct_by_priority = 0
            intermediate_correct = 0
            should_be_correct = question.question.answers_number
            incorrect_chosen = 0
            correct_not_chosen = 0
            found_error = False
            for answer in answers:
                for _id, chosen in answers_dict.items():
                    if answer.id == _id:
                        print('comparing ' + str(answer.id) + ' and ' + str(_id))
                        if answer.answer.correct == chosen:
                            print('it\'s correct')
                            if found_error is False:
                                intermediate_correct_by_priority += 1
                            intermediate_correct += 1
                            print(intermediate_correct_by_priority)
                        else:

                            print('it is incorrect')
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
                return Response({'status': 'all ok'})
            else:
                if incorrect_chosen > 0:
                    print(intermediate_correct_by_priority)
                    priority_list = []
                    for answer in answers:
                        priority_list.append(answer.answer.priority)
                    print('priority_list: ' + str(priority_list))
                    priority = heapq.nsmallest(intermediate_correct_by_priority + 1, priority_list)
                    print('curr_priorities: ' + str(priority))
                    print('question ' + str(answers.filter(answer__priority=priority[-1])) + ' failed')
                    print('your answer is incorrect (some incorrect chosen)')
                    # print(correct_answer.current_result)
                    if question.attempts_number:
                        print('previous number of attempts is ', end='')
                        print(question.attempts_number)

                        question.attempts_number = question.attempts_number - 1
                        if question.attempts_number == 0:
                            for answer in answers:
                                question.result += answer.current_result
                            question.finished = True
                            question.save()
                            answers.delete()
                            return Response({'status': 'attempts are over'})
                        print('current number of attempts is ', end='')
                        print(question.attempts_number)
                        question.save()
                    for answer in answers.filter(blocked=False):
                        if answer.blocked is False:
                            answer.current_result = answer.current_result // 2
                            answer.save()
                        print('current result of answer is ' + str(answer.current_result))
                        # answer.save()

                    result_sum = 0
                    blocked_sum = 0
                    for answer in answers.filter(blocked=True):
                        blocked_sum += answer.current_result
                    print('blocked sum is: ' + str(blocked_sum))
                    for answer in answers.filter(blocked=False):
                        result_sum += answer.current_result
                        print('current r_s:' + str(result_sum))
                    if result_sum == 0:
                        print(result_sum)
                        question.result = blocked_sum
                        question.finished = True
                        question.save()
                        answers.delete()
                        return Response({'status': 'all results are zero'})
                    priority = heapq.nsmallest(intermediate_correct_by_priority + 1, priority_list)
                    incor_ans = answers.get(answer__priority=priority[-1])
                    incor_ans.will_send_hint = True
                    incor_ans.save()
                    return Response({'status': 'incorrect chosen'})
                else:
                    print('int_cor_by_prior ' + str(intermediate_correct_by_priority))
                    print('int_cor ' + str(intermediate_correct))
                    priority_list = []
                    for answer in answers:
                        priority_list.append(answer.answer.priority)
                    print('priority_list: ' + str(priority_list))
                    priority = heapq.nsmallest(intermediate_correct_by_priority + 1, priority_list)
                    print('curr_priorities: ' + str(priority))
                    print('question ' + str(answers.filter(answer__priority=priority[-1])) + ' failed')
                    print('your answer is incorrect (not all chosen)')

                    # print(correct_answer.current_result)
                    if question.attempts_number:
                        print('previous number of attempts is ', end='')
                        print(question.attempts_number)
                        question.attempts_number = question.attempts_number - 1
                        if question.attempts_number == 0:
                            for answer in answers:
                                question.result += answer.current_result
                            question.finished = True
                            question.save()
                            answers.delete()
                            return Response({'status': 'attempts are over'})
                        print('current number of attempts is ', end='')
                        print(question.attempts_number)
                        question.save()
                    for i in range(1, len(answers_dict) + 1):
                        # answer = answers.get(answer__priority = i, answer__correct = True)
                        priority = heapq.nsmallest(i, priority_list)
                        print('curr priority_list: ' + str(priority))
                        answer = answers.filter(answer__priority=priority[-1])
                        print('curr priority: ' + str(priority[-1]))
                        if answer:
                            answer = answer.first()
                            print('going to block ' + str(answer))
                            if answers_dict[answer.id] is True and answer.answer.correct is True:
                                print('blocked')
                                answer.blocked = True
                                answer.save()
                                print('is blocked: ' + str(answer.blocked))
                                continue
                            print('is blocked: ' + str(answer.blocked))
                    print('ended blocking')
                    for answer in answers.filter(blocked=False):
                        print(str(answer) + ' is blocked: ' + str(answer.blocked))
                        if answer.blocked is False:
                            answer.current_result = answer.current_result // 2
                            answer.save()
                        print('current result of answer is ' + str(answer.current_result))
                        # answer.save()
                        # well, idk why but in case of unnecessary(extra) savings just in case, it drops
                        # some field's values to default, similar to described here
                        # https://code.djangoproject.com/ticket/27335?cversion=0&cnum_hist=3

                    result_sum = 0
                    blocked_sum = 0
                    for answer in answers.filter(blocked=True):
                        blocked_sum += answer.current_result
                    print('blocked sum is: ' + str(blocked_sum))
                    for answer in answers.filter(blocked=False):
                        result_sum += answer.current_result
                        print('current r_s:' + str(result_sum))
                    if result_sum == 0:
                        print(result_sum)
                        question.result = blocked_sum
                        question.finished = True
                        question.save()
                        answers.delete()
                        return Response({'status': 'all results are zero'})

                    priority = heapq.nsmallest(intermediate_correct_by_priority + 1, priority_list)
                    incor_ans = answers.get(answer__priority=priority[-1])
                    if incor_ans:
                        incor_ans.will_send_hint = True
                        incor_ans.save()
                    return Response({'status': 'not all corrects chosen'})

    def get_queryset(self):
        question = SessionQuestion.objects.all().get(id=self.request.query_params.get('id'))
        if question:
            answers = SessionAnswer.objects.all().filter(sessionQuestion=question, answer__deleted = False)
            return answers
        return Answer.objects.none()

class CourseTokenAjaxViewset(viewsets.ModelViewSet):
        queryset = Course.objects.all()
        serializer_class = CourseTokenAjaxSerializer
        permission_classes = (IsAuthenticated,)
        http_method_names = ['post']

        def isTokenAvaliable(self, token):
            token = Course.objects.all().filter(token = token)
            #print(token.first())
            if(token.first()):
                #print('token found')
                return False
            else:
                #print('token not found')
                return True


        def create(self, request, *args, **kwargs):
            token = self.request.data['token']
            if self.isTokenAvaliable(token):
                return Response({'avaliable' : 'true'}) # TODO change to bool
            else:
                return Response({'avaliable' : 'false'})
