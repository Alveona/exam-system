from rest_framework import routers
from .views import SessionViewSet, SessionQuestionViewSet, SessionAnswerViewSet, \
    SessionStatsViewSet, CourseTokenAjaxViewset

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'session', SessionViewSet)
router.register(r'session-q', SessionQuestionViewSet)
router.register(r'session-a', SessionAnswerViewSet)
router.register(r'stats-session', SessionStatsViewSet)
router.register(r'token-check', CourseTokenAjaxViewset)

urlpatterns = router.urls
