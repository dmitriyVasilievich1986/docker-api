from api.support_classes import (
    ReadOnlyOrAdmin,
    AuthenticatedUser,
    get_user_from_by_code,
)
from rest_framework import viewsets, response, decorators, permissions, serializers
from django.shortcuts import get_object_or_404
from .serializer import BlogSerializer
from user.models import User
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
        # context["get_comments"] = instance.get_comments
        context["get_parent"] = instance.get_parent
        return response.Response(context)

    @decorators.action(
        permission_classes=[permissions.AllowAny],
        methods=["POST"],
        detail=True,
    )
    def likes(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(klass=Blog, name=pk)
        r = get_user_from_by_code(request)
        if r.status_code >= 300:
            raise serializers.ValidationError(detail=r.text)
        user = User.objects.filter(id=r.json()["id"]).first()

        is_liked = user in instance.likes.all()
        if is_liked:
            instance.likes.remove(user)
        else:
            instance.likes.add(user) if user else instance.likes.create(
                id=r.json()["id"]
            )

        context = {
            "likes": instance.get_likes_count,
            "is_liked": not is_liked,
        }
        return response.Response(context)

    @decorators.action(
        methods=["GET"],
        detail=True,
    )
    def get_by_name(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(klass=Blog, name=pk)
        serializer = self.get_serializer(instance)
        context = serializer.data
        context["is_liked"] = request.user in instance.likes.all()
        # context["get_comments"] = instance.get_comments
        context["get_parent"] = instance.get_parent
        return response.Response(context)