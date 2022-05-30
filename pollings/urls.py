from django.urls import path, include
from rest_framework_nested import routers
from pollings import views

app_name = "pollings"

router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet, basename="users")
router.register(r'questions', views.QuestionViewSet, basename='questions')

questions_router = routers.NestedSimpleRouter(router, r'questions', lookup='question')
questions_router.register(r'answers', views.AnswerViewSet, basename='question-answers')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(questions_router.urls))
]
