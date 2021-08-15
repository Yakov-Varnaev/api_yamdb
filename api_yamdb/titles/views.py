from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from .models import Category
from .serializers import CategorySerializer
from .permissions import IsAdminOrReadOnly

class CategoryViewSet(mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.CreateModelMixin,
                      GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    search_fields = ('name',)
