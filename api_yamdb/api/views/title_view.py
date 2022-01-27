from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from api.filters import TitleFilter
from api.permissions import AdminOrReadOnly
from api.serializers.title_serializer import (TitleSerializerRead,
                                              TitleSerializerWrite)
from reviews.models import Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_class = TitleFilter
    ordering = ('id',)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleSerializerWrite
        return TitleSerializerRead
