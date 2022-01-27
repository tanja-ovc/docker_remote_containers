from rest_framework import filters

from api.mixins import ListCreateDestroyMixin
from api.permissions import AdminOrReadOnly
from api.serializers import GenreSerializer
from reviews.models import Genre


class GenreViewSet(ListCreateDestroyMixin):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name',)
    ordering = ('name',)
