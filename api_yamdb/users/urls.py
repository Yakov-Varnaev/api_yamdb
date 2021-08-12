from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserModelViewset, SignupView

router = DefaultRouter()
router.register('users', UserModelViewset)

urlpatterns= [
    path('', include(router.urls)),
    path('auth/signup/', SignupView.as_view()),
]