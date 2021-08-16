from rest_framework import routers

from django.urls import path, include
from .views import ReviewViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/rewiews', ReviewViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/rewiews/(?P<review_id>\d+)', CommentViewSet
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
