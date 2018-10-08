from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
import secrets  # used to do a safe random choice of questions
import random
from .models import Question, Course, Answer, UserCourseRelation, Profile, CourseSession, \
    SessionQuestion, SessionAnswer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        # print(self.context['request'].data['data1'])
        users = User.objects.all().filter(username=self.context['request'].data['username'])
        if not users:
            user = User.objects.create_user(username=self.context['request'].data['username'],
                                            password=self.context['request'].data['password'])
        else:
            return serializers.ValidationError('Username is already taken')
        profile = Profile(user=user)
        if 'image' in validated_data:
            profile.image = validated_data['image']
        if 'phone' in validated_data:
            profile.phone = validated_data['phone']
        if 'group' in validated_data:
            profile.group = validated_data['group']
        if 'activity' in validated_data:
            profile.activity = validated_data['activity']
        profile.save()
        return profile

    class Meta:
        model = Profile
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
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


class CourseSerializer(serializers.ModelSerializer):
    subscribed = serializers.SerializerMethodField()
    extra_kwargs = {
        'url': {'view_name': 'courses', 'lookup_field': 'token'}
    }

    def create(self, validated_data):
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
        questions_to_parse = validated_data['questions']
        print(questions_to_parse)
        print(type(questions_to_parse))
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
        # TODO RETURN 'SUBSCRIBED' FIELD IN JSON
        model = Course
        fields = ('id', 'name', 'description', 'author', 'token', 'image'
                  , 'questions_number', 'attempts', 'subscribed', 'questions')

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


class SessionSerializer(serializers.ModelSerializer):
    '''perfect_mark = serializers.SerializerMethodField()
    good_mark = serializers.SerializerMethodField()
    satisfactory_mark = serializers.SerializerMethodField()
    session_questions = serializers.SerializerMethodField() '''  # TODO STATS

    def create(self, validated_data):

        # DEBUG :
        ''''''''''''
        CourseSession.objects.all().delete()
        SessionQuestion.objects.all().delete()
        SessionAnswer.objects.all().delete()
        ''''''''''''

        course = Course.objects.all().get(token=self.context['request'].data['token'])
        # print(course.questions)
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

            attempts = [attempt_number for attempt_number in [session for session in sessions]]
            if attempts:
                number_of_attempts = max(attempts)
            else:
                number_of_attempts = 0
            print('number of attempts: ', end='')
            print(number_of_attempts)

            if number_of_attempts >= course.attempts:
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
                                            result=0, attempts_number=0,
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
                                              current_result = answer.weight)
                    session_a.save()
                    print('s_a created: ', end='')
                    print(session_a)
        return session

    class Meta:
        model = CourseSession
        fields = '__all__'


class SessionQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = SessionQuestion
        fields = '__all__'


class SessionAnswerSerializer(serializers.ModelSerializer):
    answer = AnswerInCourseSerializer(read_only=True)

    # hint = serializers.SerializerMethodField()
    # audio_hint = serializers.SerializerMethodField()
    '''
    def create(self, validated_data):
        # course =    CourseSession.objects.all().get(user = self.request.user, course__token =
        # self.context['request'].data['token'], finished = False)
        question = SessionQuestion.objects.all().get(id=self.context['request'].data['id'])
        answers_list = self.context['request'].data['answers']
        print(answers_list)
        print('answer_type: ', end='')
        print(question.question.answer_type)
        answers_of_question = SessionAnswer.objects.all().filter(sessionQuestion=question, blocked = False)
        if question.question.answer_type == 1:
            print(SessionAnswer.objects.all().get(sessionQuestion=question))
            correct_answer = SessionAnswer.objects.all().get(sessionQuestion=question)
            print('correct answer is ', end='')
            print(correct_answer.answer.text)
            if answers_list[0] == correct_answer.answer.text:
                print('your answer is correct')
                correct_answer.blocked = True
                correct_answer.save()

                question.result += correct_answer.current_result
                question.save()
                serializer = SessionAnswerSerializer(correct_answer, data = None)
                if serializer.is_valid():
                    return serializer.save().data
                #return correct_answer
            else:
                print('your answer is incorrect')
                print('previous number of attempts is ', end='')
                print(question.attempts_number)
                question.attempts_number = question.attempts_number - 1
                print('current number of attempts is ', end='')
                print(question.attempts_number)
                question.save()
                correct_answer.current_result = correct_answer.current_result / 2
                correct_answer.save()
                serializer = SessionAnswerSerializer(correct_answer,data = None)
                if serializer.is_valid():
                    return serializer.save().data'''


    # def get_hint(self, obj):

    # def get_audio_hint(self, obj):

    class Meta:
        model = SessionAnswer
        fields = '__all__'
