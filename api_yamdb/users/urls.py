from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserModelViewset, SignupView, CodeConfirmView
from .router import MyUserUsernameRouter

us_rout = MyUserUsernameRouter()
us_rout.register('users_________', UserModelViewset)
router = DefaultRouter()
router.register('users', UserModelViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', SignupView.as_view()),
    path('auth/token/', CodeConfirmView.as_view()),
]

for url in us_rout.urls:
    print(url)