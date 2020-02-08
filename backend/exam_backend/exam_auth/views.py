from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers, views
from exam_auth.models import Profile
from exam_auth.serializers import ProfileSerializer, AccountSerializer
from django.contrib.auth.models import User

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'patch', 'delete', 'post']

    def get_queryset(self):
        user = self.request.user
        if self.request.method == "GET":
            queryset = Profile.objects.all()
            return [AccountSerializer(profile).data for profile in queryset]

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

# class 

# class RegisterViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     http_method_names = ['post']

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = AccountSerializer
    http_method_names = ['post', 'put']

    def create(self, request):
        username = request.data.get('username')
        if Profile.objects.all().filter(user__username = username):
            return Response({"message":"Username has already been taken"}, 400)
        password = request.data.get('password')
        activity = request.data.get('activity')
        name = request.data.get('name')
        surname = request.data.get('surname')
        image = request.data.get('image')
        phone = request.data.get('phone')
        group = 'Студент'
        user = User.objects.create_user(username = username, password=password)
        user.save()
        profile = Profile(user = user, name = name, surname = surname,
                         activity = activity, image = image, 
                         phone = phone, group = group)
        profile.save()
        return Response(AccountSerializer(profile).data, 201)

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        if not profile:
            return Response({"message":"Profile not found"}, 404)
        
        profile.activity = request.data.get('activity')
        profile.name = request.data.get('name')
        profile.surname = request.data.get('surname')
        profile.image = request.data.get('image')
        profile.phone = request.data.get('phone')
        profile.save()
        return Response(AccountSerializer(profile).data, 200)

class PersonalProfileView(views.APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'patch', 'delete', 'post']

    def get(self, request):
        user = self.request.user
        if self.request.method == "GET":
            profile = Profile.objects.all().filter(user=user).first()
        
            if not profile:
                return Response({"message":"Profile not found"}, 404)
            return Response(AccountSerializer(profile).data, 200)
        
class TeacherPromotionView(views.APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']

    def post(self, request):
        user = self.request.user
        profile = Profile.objects.all().filter(user=user).first()
        if profile.group < 2:
            return Response({"message":"Access denied"}, 403)

        profile_to_find = request.data.get('user')
        profile = Profile.objects.all().filter(id=profile_to_find).first()
    
        if not profile:
            return Response({"message":"Profile not found"}, 404)
        
        if profile.group == 0:
            profile.group = 1
            profile.save()
            return Response(AccountSerializer(profile).data, 200)

        if profile.group == 1:
            profile.group = 0
            profile.save()
            return Response(AccountSerializer(profile).data, 200)        
        
