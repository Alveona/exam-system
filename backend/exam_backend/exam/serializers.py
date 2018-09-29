from rest_framework import serializers
from .models import Question, Course, Answer, UserCourseRelation

class QuestionSerializer(serializers.ModelSerializer):


    def create(self, validated_data):
        question = Question(user = self.context['request'].user, title = validated_data['title'],
                            text = validated_data['text'],  answer_type = validated_data['answer_type'],
                            difficulty=validated_data['difficulty'],
                            comment=validated_data['comment'],
                            )
        try:
            question.image= validated_data['image']
        except:
            print('Exception during image upload')
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
    def create(self, validated_data):
        course = Course(name = validated_data['name'], description = validated_data['description'],
                        questions_number = validated_data['questions_number'])
        course.save()
        for question in validated_data['questions']:
            course.questions.add(question)
        try:
            course.image= validated_data['image']
        except:
            print('Exception during image upload')
        #if validated_data['image'] is not None:
            #course.image.add(validated_data['image'])
             #print("DATA " + validated_data['image'])
        #course.user.set(user_relation)
        #course.save()
        user_relation = UserCourseRelation(user=self.context['request'].user, course = course, access=1)
        user_relation.save()
        course.save()
        return course
    class Meta:
        model = Course
        fields = '__all__'