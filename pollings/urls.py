from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from pollings import views
from pollings.views import RegisterView

app_name = "pollings"

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet, basename="users")
router.register(r'questions', views.QuestionViewSet, basename='questions')

questions_router = routers.NestedSimpleRouter(router, r'questions', lookup='question')
questions_router.register(r'answers', views.AnswerViewSet, basename='question-answers')

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh',  TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('', include(questions_router.urls))
]
