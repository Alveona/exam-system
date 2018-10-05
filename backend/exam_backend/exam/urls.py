from rest_framework import routers
from .views import QuestionViewSet, AnswerViewSet, CourseViewSet, QuestionListViewSet, \
    ProfileViewSet, RegisterViewSet, CourseCreatedViewSet, CourseAddedViewSet

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'questions', QuestionViewSet, base_name='questions')
router.register(r'questionslist', QuestionListViewSet)
router.register(r'register', RegisterViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'courses-created', CourseCreatedViewSet)
router.register(r'courses-added', CourseAddedViewSet)
urlpatterns = router.urls