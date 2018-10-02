from rest_framework import serializers
from .models import Question, Course, Answer, UserCourseRelation


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

    class Meta:
        model = Course
        fields = '__all__'
