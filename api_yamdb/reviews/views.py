from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .serializers import ReviewSerializer, CommentSerializer
from .permissions import AuthorModeratorAdminOrReadOnly
from .models import Review, Comment
from titles.models import Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AuthorModeratorAdminOrReadOnly,
    ]
    # 4. Тут лучше получить не только id, но и сам объекь
    # 5. А что если я сделаю запрос на страницу к тайтлу, которого нет?
    #    подумай, как обработать это исключение.
    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    # 6. Тут тоже надо получить объект и передавать в метод .save() объект,
    # а не только id
    # 7. В DRF есть неплохая штука CurrentUserDefault, напрямую
    # использовать ее ты не сможешь. Но ты можешь подсмотреть, как реализовать этот
    # функционал тут: http://www.django-rest-framework.org/api-guide/validators/#currentuserdefault
    # если не ошибаюсь, то тма должен быть код реализации этой штуки
    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user, title_id=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AuthorModeratorAdminOrReadOnly,
    ]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        serializer.save(author=self.request.user, review_id=review_id)
