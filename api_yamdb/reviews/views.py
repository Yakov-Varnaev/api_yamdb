from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from .serializers import ReviewSerializer, CommentSerializer
from .permissions import AuthorModeratorAdminOrReadOnly
from .models import Review, Comment


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModeratorAdminOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorModeratorAdminOrReadOnly,) # im not sure, but i think you wont ve able to use or '|' if you use () instead of []

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
