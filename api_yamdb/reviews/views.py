from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from rest_framework import viewsets, permissions

from .serializers import ReviewSerializer, CommentSerializer
from .models import Review
from api_yamdb.permissions import AuthorModeratorAdminOrReadOnly
from titles.models import Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AuthorModeratorAdminOrReadOnly,
    ]

    @cached_property
    def title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.title.reviews.all()

    def perform_create(self, serializer):
        title = self.title
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AuthorModeratorAdminOrReadOnly,
    ]

    @cached_property
    def review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        return self.review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.review)
