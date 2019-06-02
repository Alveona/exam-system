from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
from exam_auth.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

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
