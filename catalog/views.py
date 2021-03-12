from rest_framework import viewsets, response, decorators
from api.support_classes import ReadOnlyOrAdmin
from django.shortcuts import get_object_or_404
from .serializer import CatalogSerializer
from .models import Catalog


class CatalogViewSet(viewsets.ModelViewSet):
    serializer_class = CatalogSerializer
    queryset = Catalog.objects.all()
    permission_classes = [ReadOnlyOrAdmin]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        context = serializer.data
        context["get_child"] = instance.get_child
        context["get_parent"] = instance.get_parent
        return response.Response(context)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(serializer.data)

    @decorators.action(
        detail=True,
        methods=["GET"],
    )
    def get_by_name(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(klass=Catalog, name=pk)
        serializer = self.get_serializer(instance)
        context = serializer.data
        context["get_child"] = instance.get_child
        context["get_parent"] = instance.get_parent
        return response.Response(context)