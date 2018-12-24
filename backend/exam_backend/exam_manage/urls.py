from rest_framework import routers
from .views import QuestionViewSet, AnswerViewSet, CourseViewSet, QuestionListViewSet, \
    CourseCreatedViewSet, CourseAddedViewSet, RelationViewSet, \
    RelationUnsubscribeViewSet, \
    AnswerFormDataViewSet

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

urlpatterns = router.urls
