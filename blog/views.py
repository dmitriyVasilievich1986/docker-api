from rest_framework import viewsets, response, decorators, permissions
from api.support_classes import ReadOnlyOrAdmin
from django.shortcuts import get_object_or_404
from .serializer import BlogSerializer
from .models import Blog


class BlogViewSet(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [ReadOnlyOrAdmin]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        context = serializer.data
        context["is_liked"] = request.user in instance.likes.all()
        context["get_comments"] = instance.get_comments
        context["get_parent"] = instance.get_parent
        return response.Response(context)

    @decorators.action(
        detail=True,
        methods=["POST"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def likes(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(klass=Blog, name=pk)

        is_liked = request.user in instance.likes.all()
        if is_liked:
            instance.likes.remove(request.user)
        else:
            instance.likes.add(request.user)

        context = {
            "likes": instance.get_likes_count,
            "is_liked": not is_liked,
        }
        return response.Response(context)

    @decorators.action(
        detail=True,
        methods=["GET"],
    )
    def get_by_name(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(klass=Blog, name=pk)
        serializer = self.get_serializer(instance)
        context = serializer.data
        context["is_liked"] = request.user in instance.likes.all()
        context["get_comments"] = instance.get_comments
        context["get_parent"] = instance.get_parent
        return response.Response(context)