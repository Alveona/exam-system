from rest_framework import routers
from .views import QuestionViewSet, AnswerViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
urlpatterns = router.urls