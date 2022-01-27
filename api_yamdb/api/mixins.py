from rest_framework import mixins, viewsets


class ListCreateDestroyMixin(mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    pass
