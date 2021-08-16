from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Category, Genre, Title
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          TitleCreateSerializer)
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
    search_fields = ('name',)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]


class GenreViewSet(RetrieveCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    search_fields = ('name',)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]


class TitleViewSet(ModelViewSet):
    serializer_class = TitleSerializer
    filterset_fields = ('year',)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]

    def get_serializer(self, *args, **kwargs):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer(*args, **kwargs)
        return self.serializer_class(*args, **kwargs)

    def get_queryset(self):
        genre_category_filters = {}
        genre_category_filters['genre__slug'] = (
            self.request.query_params.get('genre')
        )
        genre_category_filters['category__slug'] = (
            self.request.query_params.get('category')
        )
        genre_category_filters['name__contains'] = (
            self.request.query_params.get('name')
        )
        genre_category_filters = {
            k: v for k, v in genre_category_filters.items()
            if v is not None
        }
        print(genre_category_filters)
        return (
            Title.objects
            .prefetch_related('genre')
            .select_related('category')
            .filter(**genre_category_filters)
        )
