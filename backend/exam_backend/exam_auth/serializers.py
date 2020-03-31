from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
from exam_auth.models import Profile
from exam_manage.models import QuestionsSubscriptionRelation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    subscribed = serializers.SerializerMethodField()
    # group = serializers.SerializerMethodField()

    def create(self, validated_data):
        users = User.objects.all().filter(
            username=self.context["request"].data["username"]
        )
        if not users:
            user = User.objects.create_user(
                username=self.context["request"].data["username"],
                password=self.context["request"].data["password"],
            )
        else:
            return serializers.ValidationError("Username is already taken")
        profile = Profile(user=user)
        if "image" in validated_data:
            profile.image = validated_data["image"]
        if "name" in validated_data:
            profile.name = validated_data["name"]
        if "surname" in validated_data:
            profile.surname = validated_data["surname"]
        if "phone" in validated_data:
            profile.phone = validated_data["phone"]
        if "activity" in validated_data:
            profile.activity = validated_data["activity"]
        profile.save()
        return profile

    class Meta:
        model = Profile
        fields = "__all__"

    def get_subscribed(self, obj):
        subcsription = QuestionsSubscriptionRelation.objects.filter(
            subscriber=self.context["request"].user,
            subscription__Profile_User=obj["id"],
        )
        if subcsription:
            return True
        return False


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    group = serializers.SerializerMethodField()
    has_user_list_access = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "name",
            "surname",
            "activity",
            "image",
            "phone",
            "group",
            "has_user_list_access",
        )

    def get_group(self, obj):
        if obj.group == -1:
            return "demo"
        if obj.group == 0:
            return "student"
        if obj.group == 1:
            return "teacher"
        if obj.group == 2:
            return "admin"

    def get_has_user_list_access(self, obj):
        if obj.group > 1:
            return True
        return False
