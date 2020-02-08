from rest_framework import routers
from .views import ProfileViewSet, RegisterViewSet, PersonalProfileView, TeacherPromotionView
from django.urls import path

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'register', RegisterViewSet)
router.register(r'profile', RegisterViewSet)
router.register(r'profiles', ProfileViewSet)
# router.register(r'my', PersonalProfileView.as_view())

urlpatterns = router.urls
urlpatterns += path('my', PersonalProfileView.as_view()),
urlpatterns += path('promote', TeacherPromotionView.as_view()),
