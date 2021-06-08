from api.support_classes import (
    ReadOnlyOrAdmin,
    AuthenticatedUser,
    get_user_by_token,
)
from rest_framework import viewsets, response, decorators, permissions, serializers
from django.shortcuts import get_object_or_404
from .serializer import BlogSerializer
from user.models import User
from .models import Blog

# import logging

# logger = logging.getLogger("api")


class BlogViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnlyOrAdmin]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def _get_blog(self, request, instance, *args, **kwargs):
        user = get_user_by_token(request, raise_error=False)
        serializer = self.get_serializer(instance)

        context = serializer.data
        context["is_liked"] = user in instance.likes.all()
        context["comments"] = instance.get_comments
        context["get_parent"] = instance.get_parent

        if user and user not in instance.views.all():
            instance.views.add(user)
        return response.Response(context)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return self._get_blog(request, instance)

    @decorators.action(
        methods=["GET"],
        detail=True,
    )
    def get_by_name(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(klass=Blog, name=pk)
        return self._get_blog(request, instance)

    @decorators.action(
        permission_classes=[permissions.AllowAny],
        methods=["POST"],
        detail=True,
    )
    def likes(self, request, pk=None, *args, **kwargs):

        instance = get_object_or_404(klass=Blog, name=pk)
        user = get_user_by_token(request)

        is_liked = user in instance.likes.all()
        instance.likes.remove(user) if is_liked else instance.likes.add(user)

        context = {
            "likes": instance.get_likes_count,
            "is_liked": not is_liked,
        }
        return response.Response(context)
