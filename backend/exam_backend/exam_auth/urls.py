from rest_framework import routers
from .views import ProfileViewSet, RegisterViewSet

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'register', RegisterViewSet)
router.register(r'profile', ProfileViewSet)

urlpatterns = router.urls
