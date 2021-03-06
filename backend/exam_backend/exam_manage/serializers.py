from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
from .models import (
    Question,
    Course,
    Answer,
    UserCourseRelation,
    StrictMode,
    Hint,
    QuestionMedia,
)
from exam.models import CourseSession
from exam_backend.utils import upload_media_file


class QuestionSerializer(serializers.ModelSerializer):
    can_manage = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = "__all__"

    def get_can_manage(self, obj):
        if not self.context.get("request"):
            return None
        return obj.user == self.context["request"].user


class QuestionListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    can_manage = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ("id", "title", "text", "answer_type", "author", "can_manage")

    def get_author(self, obj):
        if obj.user:
            return {
                "name": obj.user.Profile_User.name,
                "surname": obj.user.Profile_User.surname,
            }
        return {"name": "", "surname": ""}

    def get_can_manage(self, obj):
        if not self.context.get("request"):
            return None
        return obj.user == self.context["request"].user


class AnswerInCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "text", "weight", "image", "priority")


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class AnswerFormDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    subscribed = serializers.SerializerMethodField()
    mode = serializers.SerializerMethodField()
    extra_kwargs = {"url": {"view_name": "courses", "lookup_field": "token"}}

    current_attempt = serializers.SerializerMethodField()

    def create(self, validated_data):

        questions_to_parse = validated_data["questions"]

        course = Course(
            name=validated_data["name"],
            description=validated_data["description"],
            questions_number=validated_data["questions_number"],
            token=validated_data["token"],
            attempts=validated_data["attempts"],
            author=validated_data["author"],
        )
        course.perfect_mark = self.context["request"].data["perfect_mark"]
        course.good_mark = self.context["request"].data["good_mark"]
        course.satisfactory_mark = self.context["request"].data["satisfactory_mark"]
        if self.context["request"].data["perfect_audio"] != "null":
            course.perfect_audio = self.context["request"].data["perfect_audio"]
        if self.context["request"].data["good_audio"] != "null":
            course.good_audio = self.context["request"].data["good_audio"]
        if self.context["request"].data["satisfactory_audio"] != "null":
            course.satisfactory_audio = self.context["request"].data[
                "satisfactory_audio"
            ]
        if self.context["request"].data["bad_audio"] != "null":
            course.bad_audio = self.context["request"].data["bad_audio"]
        if self.context["request"].data["video"] != "null":
            course.video = self.context["request"].data["video"]
        course.save()

        if questions_to_parse:
            for question in questions_to_parse:
                course.questions.add(question)

        if "image" in validated_data:
            course.image = validated_data["image"]

        if "user" in validated_data:
            user = validated_data["user"]
        else:
            user = self.context["request"].user

        user_relation = UserCourseRelation(user=user, course=course, access=1)
        user_relation.save()
        course.save()
        return course

    def partial_update(self, instance, validated_data):
        pass  # TODO

    def get_subscribed(self, obj):

        course = Course.objects.all().filter(token=obj.token).first()
        try:
            user = self.context.get('request').user
        except:
            return False
        subscribed_course = UserCourseRelation.objects.all().filter(
            access=0, course=course, user=user
        )

        if not subscribed_course:
            return False
        return True

    def get_demo_allowed(self, obj):

        if not obj.get_demo_allowed:
            return False
        return True

    def get_mode(self, obj):
        if not self.context.get("request"):
            return None
        session = CourseSession.objects.all().filter(
            course=obj, user=self.context["request"].user, finished=False
        )

        if session:
            return session.first().mode.id
        else:
            return None

    def get_current_attempt(self, obj):
        if not self.context.get("request"):
            return 0
        sessions = CourseSession.objects.all().filter(
            course=obj, user=self.context["request"].user, finished=True
        )
        attempts = [s.attempt_number for s in [session for session in sessions]]

        if attempts:
            return max(attempts)
        else:
            return 0

    class Meta:
        model = Course

        fields = "__all__"


class RelationSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        course = (
            Course.objects.all()
            .filter(token=self.context["request"].data["token"])
            .first()
        )
        relation = UserCourseRelation.objects.filter(user=self.context["request"].user, course= course, access=0)
 
        if not relation: 
            relation = UserCourseRelation(
                    user=self.context["request"].user, course=course, access=0
            )
            relation.save()
        else:
            relation.delete()
        return relation  

    class Meta:
        model = UserCourseRelation
        fields = "__all__"
        extra_kwargs = {"user": {"required": False}, "course": {"required": False}}
        validators = []  # Remove a default "unique together" constraint.


class RelationUnsubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourseRelation
        fields = "__all__"


class CourseCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "token",
            "name",
            "author",
            "user",
            "description",
            "image",
            "demo_allowed",
        )

    def get_demo_allowed(self, obj):

        if not obj.get_demo_allowed:
            return False
        return True


class CourseAddedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("token", "name", "user", "description", "image")


class StrictModeSerializer(serializers.ModelSerializer):

    class Meta:
        model = StrictMode
        fields = "__all__"

    def create(self, validated_data):
        mode = StrictMode(
            user=self.context["request"].user, name=validated_data["name"]
        )
        if "image" in validated_data:
            mode.image_url = upload_media_file(validated_data["image"])
        if "text" in validated_data:
            mode.text = validated_data["text"]
        mode.save()
        return mode


class QuestionMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionMedia
        fields = "__all__"


class HintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hint
        fields = "__all__"

