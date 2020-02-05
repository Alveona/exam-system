from rest_framework import routers
from .views import QuestionViewSet, AnswerViewSet, CourseViewSet, QuestionListViewSet, \
    CourseCreatedViewSet, CourseAddedViewSet, RelationViewSet, \
    RelationUnsubscribeViewSet, \
    AnswerFormDataViewSet, StrictModeViewSet, QuestionMediaViewSet, HintViewSet, \
    UserSubcsriptionView
from django.urls import path

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
router.register(r'strict_modes', StrictModeViewSet)
router.register(r'questions_media', QuestionMediaViewSet)
router.register(r'answers_hint', HintViewSet)


urlpatterns = router.urls
urlpatterns += path('subscribe', UserSubcsriptionView.as_view()),

