from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from exam_auth.models import Profile
from exam_auth.serializers import ProfileSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'patch', 'delete', 'post']

    def get_queryset(self):
        user = self.request.user
        if self.request.method == "GET":
            queryset = Profile.objects.all().filter(user=user)
            return queryset

    def create(self, request, *args, **kwargs):
        validated_data = self.request.data
        profile = Profile.objects.all().get(user = self.request.user)
        if 'name' in validated_data:
            profile.name = validated_data['name']
        if 'surname' in validated_data:
            profile.surname = validated_data['surname']
        if 'activity' in validated_data:
            profile.activity = validated_data['activity']
        if 'group' in validated_data:
            profile.group = validated_data['group']
        if 'phone' in validated_data:
            profile.phone = validated_data['phone']
        if 'image' in validated_data:
            # print(validated_data['image'])
            if validated_data['image'] == 'null':
                profile.image = ''
            else:
                if validated_data['image'] != 'stay':
                    profile.image = validated_data['image']
        profile.save()
        return Response(status = status.HTTP_200_OK)


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['post']
