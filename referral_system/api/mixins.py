from rest_framework import mixins, viewsets


class RetrieveUpdateListViewSet(mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    pass
