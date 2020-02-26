from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
import secrets  # used to do a safe random choice of questions
import random
from .models import  CourseSession, SessionQuestion, SessionAnswer
from exam_manage.models import Course, Question, Answer, Hint, StrictMode, QuestionMedia
from exam_manage.serializers import QuestionSerializer, AnswerInCourseSerializer, RelationUnsubscribeSerializer, QuestionMediaSerializer

class SessionStatsSerializer(serializers.ModelSerializer):
    perfect_mark = serializers.SerializerMethodField()
    perfect_audio = serializers.SerializerMethodField()
    good_mark = serializers.SerializerMethodField()
    good_audio = serializers.SerializerMethodField()
    satisfactory_mark = serializers.SerializerMethodField()
    satisfactory_audio = serializers.SerializerMethodField()
    bad_audio = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    session_q = serializers.SerializerMethodField()

    def get_perfect_mark(self, obj):
        return obj.course.perfect_mark

    def get_perfect_audio(self, obj):
        if obj.course.perfect_audio:
            return self.context.get('request').build_absolute_uri(obj.course.perfect_audio_url)

    def get_good_mark(self, obj):
        return obj.course.good_mark

    def get_good_audio(self, obj):
        if obj.course.good_audio:
            return self.context.get('request').build_absolute_uri(obj.course.good_audio_url)

    def get_satisfactory_mark(self, obj):
        return obj.course.satisfactory_mark

    def get_satisfactory_audio(self, obj):
        if obj.course.satisfactory_audio:
            return self.context.get('request').build_absolute_uri(obj.course.satisfactory_audio_url)

    def get_bad_audio(self, obj):
        if obj.course.bad_audio:
            return self.context.get('request').build_absolute_uri(obj.course.bad_audio_url)

    def get_video(self, obj):
        if obj.course.video:
            return obj.course.video

    def get_session_q(self, obj):
        #return SessionQuestion.objects.all().filter(session = obj)
        serializer = SessionQuestionStatsSerializer(instance = SessionQuestion.objects.all().filter(session = obj), many=True)
        return serializer.data

    class Meta:
        model = CourseSession
        fields = ('perfect_mark', 'good_mark', 'satisfactory_mark', 'session_q',
                  'perfect_audio', 'good_audio', 'satisfactory_audio',
                  'bad_audio', 'video')

# class OverallStatsSerializer(serializers.ModelSerializer):



class SessionQuestionStatsSerializer(serializers.ModelSerializer):
    weight_sum = serializers.SerializerMethodField()

    def get_weight_sum(self, obj):
        question = obj.question
        answers = Answer.objects.all().filter(question = question, deleted = False)
        weight_sum = sum([answer.weight for answer in answers])
        return weight_sum

    class Meta:
        model = SessionQuestion
        fields = ('order_number', 'result', 'weight_sum')


class SessionSerializer(serializers.ModelSerializer):
    '''perfect_mark = serializers.SerializerMethodField()
    good_mark = serializers.SerializerMethodField()
    satisfactory_mark = serializers.SerializerMethodField()
    session_questions = serializers.SerializerMethodField() '''  # TODO STATS

    def create(self, validated_data):
        course = Course.objects.all().filter(token=self.context['request'].data['token']).first()
        not_finished_session = CourseSession.objects.all().filter(course=course,
                                                                  user=self.context['request'].user, finished=False)
        print('not finished session: ', end='')
        print(not_finished_session)
        if not_finished_session:
            return not_finished_session
        else:
            sessions = CourseSession.objects.all().filter(course=course,
                                                          user=self.context['request'].user, finished=True)
            print('existing sessions: ', end='')
            print(sessions)

            attempts = [s.attempt_number for s in [session for session in sessions]]
            if attempts:
                number_of_attempts = max(attempts)
            else:
                number_of_attempts = 0 # first time in this course
            print('number of attempts: ', end='')
            print(number_of_attempts)

            # 0 in attempts = inf attempts
            # so is important to check 'is not None' firstly
            # because it will not calculate '>=' and compare int to None
            if course.attempts is not None and number_of_attempts >= course.attempts:
                raise serializers.ValidationError('Попытки кончились')
            else:
                session = CourseSession(course=course, attempt_number=number_of_attempts + 1,
                                        user=self.context['request'].user, finished=False)
                print(self.context['request'].data)
                mode = StrictMode.objects.all().get(id = self.context['request'].data['mode'])
                session.mode = mode
                session.save()
                list_of_questions = course.questions.all()
                print(list_of_questions)
                question = secrets.choice(list_of_questions)
                session_q = SessionQuestion(question=question,
                                            session=session, order_number=1,
                                            result=0, attempts_number=question.attempts_number,
                                            finished=False)
                print('s_q: ', end='')
                print(session_q)
                session_q.save()
                list_of_correct_answers = list(Answer.objects.all().filter(question = question, correct = True, deleted = False))
                print('correct list: ' + str(list_of_correct_answers))
                list_of_incorrect_answers = list(Answer.objects.all().filter(question=question, correct = False, deleted = False))
                print('incorrect list: ' + str(list_of_incorrect_answers))
                list_of_answers = list_of_correct_answers
                list_of_answers += random.sample(set(list_of_incorrect_answers),
                                                           question.answers_number - len(list_of_correct_answers))
                random.shuffle(list_of_answers)
                print('list of answers: ', end='')
                print(list_of_answers)
                for answer in list_of_answers:
                    session_a = SessionAnswer(sessionQuestion=session_q, blocked=False, answer=answer,
                                              current_result = answer.weight)
                    session_a.save()
                    print('s_a created: ', end='')
                    print(session_a)
                    print(' for answer ' + str(answer))
        return session

    class Meta:
        model = CourseSession
        fields = '__all__'


class SessionQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    hint = serializers.SerializerMethodField()
    audio_hint = serializers.SerializerMethodField()
    video_hint = serializers.SerializerMethodField()
    mode_image = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()

    def get_hint(self, obj):
        print('search for hint')
        object = SessionAnswer.objects.all().filter(sessionQuestion = obj, will_send_hint = True, answer__deleted = False)
        print(object)
        if object.first():
            answer = object.first().answer
            print(answer)
            mode = obj.session.mode
            print(mode)
            #print('obj from hint: ' + str(object))
            hint = Hint.objects.all().filter(answer = answer, mode = mode)
            print(hint)
            if hint:
                print(hint.first().text)
                return hint.first().text
            else:
                return None
        else:
            return None
        # if object.first():
        #     return object.first().answer.hint
        # else:
        #     return ''

    def get_audio_hint(self, obj):
        object = SessionAnswer.objects.all().filter(sessionQuestion = obj, will_send_hint = True, answer__deleted = False)
        if object.first():
            answer = object.first().answer
            mode = obj.session.mode
            #print('obj from hint: ' + str(object))
            hint = Hint.objects.all().filter(answer = answer, mode = mode)
            if hint:
                request = self.context.get('request')
                audio_url = hint.first().audio.url
                print(hint.first().audio.url)
                return request.build_absolute_uri(audio_url)
            else:
                return None
        else:
            return None
        # object = SessionAnswer.objects.all().filter(sessionQuestion=obj, will_send_hint = True, answer__deleted = False)
        # if object.first():
        #     if object.first().answer.audio:
        #         #return object.first().answer.audio
        #         #return None
        #         print(object.first().answer.audio)
        #         request = self.context.get('request')
        #         audio_url = object.first().answer.audio.url
        #         #return str('http://172.20.10.2:8000/media/' + str(object.first().answer.audio))
        #         return request.build_absolute_uri(audio_url)
        #     else:
        #         return None
        # else:
        #     return None

    def get_video_hint(self, obj):
        object = SessionAnswer.objects.all().filter(sessionQuestion = obj, will_send_hint = True, answer__deleted = False)
        print(object)
        if object.first():
            answer = object.first().answer
            print(answer)
            mode = obj.session.mode
            print(mode)
            #print('obj from hint: ' + str(object))
            hint = Hint.objects.all().filter(answer = answer, mode = mode)
            print(hint)
            if hint:
                print(hint.first().video)
                return hint.first().video
            else:
                return None
        else:
            return None
        # object = SessionAnswer.objects.all().filter(sessionQuestion = obj, will_send_hint = True, answer__deleted = False)
        # if object.first():
        #     answer = object.first().answer
        #     mode = obj.session.mode
        #     #print('obj from hint: ' + str(object))
        #     hint = Hint.objects.all().filter(answer = answer, mode = mode)
        #     if hint:
        #         request = self.context.get('request')
        #         audio_url = hint.first().video.url
        #         return request.build_absolute_uri(audio_url)
        #     else:
        #         return None
        # else:
        #     return None
    def get_media(self, obj):
        mode_id = obj.session.mode.id
        mode = StrictMode.objects.all().get(id = mode_id)
        question_id = obj.question.id
        question = Question.objects.all().get(id = question_id)
        print(question)
        print(mode)
        media = QuestionMedia.objects.all().get(mode = mode, question = question)
        serializer = QuestionMediaSerializer(instance = media)
        return serializer.data

    def get_mode_image(self, obj):
        print('get_mode_img')
        mode_id = obj.session.mode.id
        mode = StrictMode.objects.all().get(id = mode_id)
        request = self.context.get('request')
        print(mode.image)
        return request.build_absolute_uri(mode.image.url)


    class Meta:
        model = SessionQuestion
        fields = '__all__'


class SessionAnswerSerializer(serializers.ModelSerializer):
    answer = AnswerInCourseSerializer(read_only=True)
    '''hint = serializers.SerializerMethodField()
    audio_hint = serializers.SerializerMethodField()

    def get_hint(self, obj):
        if obj.will_send_hint == True:
            return obj.answer.hint
        else:
            return ''

    def get_audio_hint(self, obj):
        if obj.will_send_hint == True:
            return obj.answer.audio
        else:
            return None'''

    class Meta:
        model = SessionAnswer
        fields = '__all__'

class CourseTokenAjaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('token')
