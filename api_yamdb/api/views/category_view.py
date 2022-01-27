from rest_framework import filters

from api.mixins import ListCreateDestroyMixin
from api.permissions import AdminOrReadOnly
from api.serializers import CategorySerializer
from reviews.models import Category


class CategoryViewSet(ListCreateDestroyMixin):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name',)
    ordering = ('name',)
