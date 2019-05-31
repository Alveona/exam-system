from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
from .models import Question, Course, Answer, UserCourseRelation, StrictMode, Hint, QuestionMedia
from exam.models import CourseSession

class QuestionSerializer(serializers.ModelSerializer):


    class Meta:
        model = Question
        fields = '__all__'


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'text', 'answer_type',)


class AnswerInCourseSerializer(serializers.ModelSerializer):
    # def get_text(self, obj):
    #     if obj.question.answer_type == 1:
    #         return ''
    #     return obj.text
    class Meta:
        model = Answer
        fields = ('id', 'text', 'weight', 'image', 'priority')


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'

class AnswerFormDataSerializer(serializers.ModelSerializer):
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
                  , 'questions_number', 'attempts', 'subscribed', 'questions', 'current_attempt',
                  'perfect_mark', 'good_mark', 'satisfactory_mark')

    def get_subscribed(self, obj):
        print(obj)
        course = Course.objects.all().filter(token=obj.token).first()
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
        course = Course.objects.all().filter(token=self.context['request'].data['token']).first()
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
        fields = '__all__'


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

class StrictModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrictMode
        fields = '__all__'
    def create(self, validated_data):
        mode = StrictMode(user = self.context['request'].user, name = validated_data['name'])
        if 'image' in validated_data:
            mode.image = validated_data['image']
        if 'text' in validated_data:
            mode.text = validated_data['text']
        mode.save()
        return mode

class QuestionMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionMedia
        fields = '__all__'


class HintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hint
        fields = '__all__'
