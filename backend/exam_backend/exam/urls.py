from rest_framework import routers
from .views import QuestionViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'questions', QuestionViewSet)
urlpatterns = router.urls