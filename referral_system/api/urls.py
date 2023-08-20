from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserAuthLoginView, UserAuthSignupView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

auth_patterns = [
    path('signup/', UserAuthSignupView.as_view()),
    path('login/', UserAuthLoginView.as_view()),
]


urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(router.urls)),
]
