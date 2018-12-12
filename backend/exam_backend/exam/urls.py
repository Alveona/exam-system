from rest_framework import routers
from .views import QuestionViewSet, AnswerViewSet, CourseViewSet, QuestionListViewSet, \
    CourseCreatedViewSet, CourseAddedViewSet, RelationViewSet, \
    SessionViewSet, SessionQuestionViewSet, SessionAnswerViewSet, RelationUnsubscribeViewSet, \
    SessionStatsViewSet, AnswerFormDataViewSet, CourseTokenAjaxViewset

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'questions', QuestionViewSet, base_name='questions')
router.register(r'questionslist', QuestionListViewSet)
router.register(r'answers_array', AnswerViewSet)
router.register(r'answers', AnswerFormDataViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'courses-created', CourseCreatedViewSet)
router.register(r'courses-added', CourseAddedViewSet)
router.register(r'course-subsc', RelationViewSet)
router.register(r'course-unsubsc', RelationUnsubscribeViewSet)
router.register(r'session', SessionViewSet)
router.register(r'session-q', SessionQuestionViewSet)
router.register(r'session-a', SessionAnswerViewSet)
router.register(r'stats-session', SessionStatsViewSet)
router.register(r'token-check', CourseTokenAjaxViewset)

urlpatterns = router.urls
