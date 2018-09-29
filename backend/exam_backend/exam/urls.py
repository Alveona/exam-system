from rest_framework import routers
from .views import QuestionViewSet, AnswerViewSet, CourseViewSet

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'courses', CourseViewSet)
urlpatterns = router.urls