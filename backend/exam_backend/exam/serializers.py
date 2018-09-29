from rest_framework import serializers
from .models import Question, Course, Answer, UserCourseRelation

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
    '''def create(self, validated_data):
        user_relation = UserCourseRelation(user = self.context['request'].user, access = 1)
        course = Course(name = validated_data['name'], description = validated_data['description'],
                        image = validated_data['image'], questions_number = validated_data['questions_number'])
        course.questions.add(validated_data['questions'][0])
        course.user.add(user_relation)
        course.save()
        return course'''
    class Meta:
        model = Course
        fields = '__all__'