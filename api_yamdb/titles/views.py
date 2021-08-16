from django.db.models import query
from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from .models import Category, Genre
from .serializers import CategorySerializer, GenreSerializer
from .permissions import IsAdminOrReadOnly


class RetrieveCreateDeleteViewSet(mixins.ListModelMixin,
                                mixins.DestroyModelMixin,
                                mixins.CreateModelMixin,
                                GenericViewSet):
    pass


class CategoryViewSet(RetrieveCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    search_fields = ('name',)


class GenreViewSet(RetrieveCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    search_fields = ('name',)
