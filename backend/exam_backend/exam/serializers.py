from rest_framework import serializers
from .models import Question, Course, Answer

class QuestionSerializer(serializers.ModelSerializer):


    def create(self, validated_data):
        question = Question(user = self.context['request'].user, title = validated_data['title'],
                            text = validated_data['text'],  answer_type = validated_data['answer_type'],
                            difficulty=validated_data['difficulty'],
                            comment=validated_data['comment'],
                            image = validated_data['image'],
                            )
        question.save()
        return question

    class Meta:
        model = Question
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'