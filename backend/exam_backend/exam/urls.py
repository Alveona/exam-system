from rest_framework import routers
from .views import QuestionViewSet, AnswerViewSet, CourseViewSet, QuestionListViewSet, \
    ProfileViewSet, RegisterViewSet, CourseCreatedViewSet, CourseAddedViewSet, RelationViewSet, \
    SessionViewSet, SessionQuestionViewSet, SessionAnswerViewSet, RelationUnsubscribeViewSet, \
    SessionStatsViewSet

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'questions', QuestionViewSet, base_name='questions')
router.register(r'questionslist', QuestionListViewSet)
router.register(r'register', RegisterViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'courses-created', CourseCreatedViewSet)
router.register(r'courses-added', CourseAddedViewSet)
router.register(r'course-subsc', RelationViewSet)
router.register(r'course-unsubsc', RelationUnsubscribeViewSet)
router.register(r'session', SessionViewSet)
router.register(r'session-q', SessionQuestionViewSet)
router.register(r'session-a', SessionAnswerViewSet)
router.register(r'stats-session', SessionStatsViewSet)

urlpatterns = router.urls