from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from rest_framework import viewsets, permissions, serializers

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
    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title

        if Review.objects.filter(
            author=self.request.user,
            title=title
        ).exists():
            raise serializers.ValidationError(
                detail=f'You have already reviewed {title.name}'
            )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AuthorModeratorAdminOrReadOnly,
    ]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
