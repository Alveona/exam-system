from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
from exam_auth.models import Profile
from exam_manage.models import QuestionsSubscriptionRelation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    subscribed = serializers.SerializerMethodField()

    def create(self, validated_data):
        users = User.objects.all().filter(username=self.context['request'].data['username'])
        if not users:
            user = User.objects.create_user(username=self.context['request'].data['username'],
                                            password=self.context['request'].data['password'])
        else:
            return serializers.ValidationError('Username is already taken')
        profile = Profile(user=user)
        if 'image' in validated_data:
            profile.image = validated_data['image']
        if 'name' in validated_data:
            profile.name = validated_data['name']
        if 'surname' in validated_data:
            profile.surname = validated_data['surname']
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

    def get_subscribed(self, obj):
        subcsription = QuestionsSubscriptionRelation.objects.filter(subscriber = self.context['request'].user, subscription = obj['id'])
        if subcsription:
            return True
        return False

class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'name', 'surname',
                'activity', 'image', 'phone', 'group')