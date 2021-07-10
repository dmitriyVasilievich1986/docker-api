from rest_framework import viewsets, response, decorators
from api.support_classes import ReadOnlyOrAdmin
from django.shortcuts import get_object_or_404
from .serializer import CatalogSerializer
from .models import Catalog


class CatalogViewSet(viewsets.ModelViewSet):
    serializer_class = CatalogSerializer
    queryset = Catalog.objects.all()
    permission_classes = [ReadOnlyOrAdmin]

    def _get_catalog(self, instance, *args, **kwargs):
        serializer = self.get_serializer(instance)
        payload = {
            **serializer.data,
            "catalog": instance.get_child,
            "parent": instance.get_parent[1:][::-1],
        }
        return payload

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        context = self._get_catalog(instance)
        return response.Response(context)

    @decorators.action(
        detail=True,
        methods=["GET"],
    )
    def by_name(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(klass=Catalog, name=pk)
        context = self._get_catalog(instance)
        return response.Response(context)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(serializer.data)
