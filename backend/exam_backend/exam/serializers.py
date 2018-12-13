from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
import secrets  # used to do a safe random choice of questions
import random
from .models import Question, Course, Answer, UserCourseRelation, CourseSession, \
    SessionQuestion, SessionAnswer


class QuestionSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        print(self.context['request'].data)
        question = Question(user=self.context['request'].user, title=validated_data['title'],
                            text=validated_data['text'], answer_type=validated_data['answer_type'])
        if 'timer' in validated_data:
            question.timer = validated_data['timer']
        if 'attempts_number' in validated_data:
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
        return question

    class Meta:
        model = Question
        fields = '__all__'


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'text', 'answer_type',)


class AnswerInCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'weight', 'image', 'priority')


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'

class AnswerFormDataSerializer(serializers.ModelSerializer):
    '''
    def create(self, validated_data):
        print(validated_data)

        question_to_parse = validated_data['question']
        print(question_to_parse)
        for q in question_to_parse:
            print(q)
        text_to_parse = validated_data['text']
        correct_to_parse = validated_data['correct']
        weight_to_parse = validated_data['weight']
        audio_to_parse = validated_data['audio']
        hint_to_parse = validated_data['hint']
        priority_to_parse = validated_data['priority']


        list_of_created_ids = []
        for i in range(0, len(question_to_parse)-1):
            answer = Answer(question = question_to_parse[i], text = text_to_parse[i],
                            correct = correct_to_parse[i], weight = weight_to_parse[i],
                            audio = audio_to_parse[i], hint = hint_to_parse[i],
                            priority = priority_to_parse[i])
            answer.save()
            print(answer)
            list_of_created_ids.append(answer.id)
        queryset = Answer.objects.all().filter(id__in = list_of_created_ids)
        return queryset
    '''
    class Meta:
        model = Answer
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    subscribed = serializers.SerializerMethodField()
    extra_kwargs = {
        'url': {'view_name': 'courses', 'lookup_field': 'token'}
    }

    current_attempt = serializers.SerializerMethodField()

    def create(self, validated_data):
        questions_to_parse = validated_data['questions']
        print(questions_to_parse)
        course = Course(name=validated_data['name'], description=validated_data['description'],
                        questions_number=validated_data['questions_number'],
                        token=validated_data['token'],
                        attempts=validated_data['attempts'],
                        author=validated_data['author'])
        course.perfect_mark = self.context['request'].data['perfect_mark']
        course.good_mark = self.context['request'].data['good_mark']
        course.satisfactory_mark = self.context['request'].data['satisfactory_mark']
        course.save()
        #questions = self.context['request'].data['questions']
        #questions_to_parse = validated_data['questions']

        if questions_to_parse:
            for question in questions_to_parse:
                course.questions.add(question)

        if 'image' in validated_data:
            course.image = validated_data['image']

        if 'user' in validated_data:
            user = validated_data['user']
        else:
            user = self.context['request'].user
        user_relation = UserCourseRelation(user=user, course=course, access=1)
        user_relation.save()
        course.save()
        return course

    def partial_update(self, instance, validated_data):
        pass  # TODO

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'author', 'token', 'image'
                  , 'questions_number', 'attempts', 'subscribed', 'questions', 'current_attempt')

    def get_subscribed(self, obj):
        print(obj)
        course = Course.objects.all().get(token=obj.token)
        print(course)
        subscribed_course = UserCourseRelation.objects.all().filter(access=0, course=course,
                                                                    user=self.context['request'].user)
        print(subscribed_course)
        if not subscribed_course:
            return False
        return True

    def get_current_attempt(self, obj):
        sessions = CourseSession.objects.all().filter(course=obj,
                                                      user=self.context['request'].user, finished=True)
        attempts = [s.attempt_number for s in [session for session in sessions]]
        if attempts:
            return max(attempts)
        else:
            return 0


class RelationSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        course = Course.objects.all().get(token=self.context['request'].data['token'])
        print(course)
        relation = UserCourseRelation(user=self.context['request'].user,
                                      course=course, access=0)
        relation.save()
        return relation  # TODO CHECK WHAT HAPPENS IF DELETE RETURN STATEMENT (WILL THERE NO RESPONSE IN POST?)

    class Meta:
        model = UserCourseRelation
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}, 'course': {'required': False}}
        validators = []  # Remove a default "unique together" constraint.

class RelationUnsubscribeSerializer(serializers.ModelSerializer):


    class Meta:
        model = UserCourseRelation
        field = '__all__'


class CourseCreatedSerializer(serializers.ModelSerializer):
    # user = RelationSerializer(read_only=True)
    class Meta:
        model = Course
        fields = ('token', 'name', 'author', 'user', 'description', 'image')


class CourseAddedSerializer(serializers.ModelSerializer):
    # user = RelationSerializer(read_only=True)
    class Meta:
        model = Course
        fields = ('token', 'name', 'user', 'description', 'image')


class SessionStatsSerializer(serializers.ModelSerializer):
    perfect_mark = serializers.SerializerMethodField()
    good_mark = serializers.SerializerMethodField()
    satisfactory_mark = serializers.SerializerMethodField()
    session_q = serializers.SerializerMethodField()

    def get_perfect_mark(self, obj):
        return obj.course.perfect_mark

    def get_good_mark(self, obj):
        return obj.course.good_mark

    def get_satisfactory_mark(self, obj):
        return obj.course.satisfactory_mark

    def get_session_q(self, obj):
        #return SessionQuestion.objects.all().filter(session = obj)
        serializer = SessionQuestionStatsSerializer(instance = SessionQuestion.objects.all().filter(session = obj), many=True)
        return serializer.data

    class Meta:
        model = CourseSession
        fields = ('perfect_mark', 'good_mark', 'satisfactory_mark', 'session_q')


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
        course = Course.objects.all().get(token=self.context['request'].data['token'])
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

    def get_hint(self, obj):
        object = SessionAnswer.objects.all().filter(sessionQuestion = obj, will_send_hint = True, answer__deleted = False)
        #print('obj from hint: ' + str(object))
        if object.first():
            return object.first().answer.hint
        else:
            return ''

    def get_audio_hint(self, obj):
        object = SessionAnswer.objects.all().filter(sessionQuestion=obj, will_send_hint = True, answer__deleted = False)
        if object.first():
            if object.first().answer.audio:
                #return object.first().answer.audio
                #return None
                print(object.first().answer.audio)
                request = self.context.get('request')
                audio_url = object.first().answer.audio.url
                #return str('http://172.20.10.2:8000/media/' + str(object.first().answer.audio))
                return request.build_absolute_uri(audio_url)
            else:
                return None
        else:
            return None

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
