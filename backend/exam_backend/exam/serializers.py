from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
from .models import Question, Course, Answer, UserCourseRelation, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', )

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    def create(self, validated_data):
        #print(self.context['request'].data['data1'])
        users = User.objects.all().filter(username = self.context['request'].data['username'])
        if not users:
            user = User.objects.create_user(username = self.context['request'].data['username'],
                                            password = self.context['request'].data['password'])
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
                            text=validated_data['text'], answer_type=validated_data['answer_type'],
                            answers_number=validated_data['answers_number'])
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
        fields = ('title', 'text', 'answer_type',)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        course = Course(name=validated_data['name'], description=validated_data['description'],
                        questions_number=validated_data['questions_number'])
        course.save()
        for question in validated_data['questions']:
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

    def update(self, instance, validated_data):
        pass
    class Meta:
        model = Course
        fields = '__all__'
