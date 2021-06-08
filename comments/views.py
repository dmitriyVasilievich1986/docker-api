from rest_framework import (
    viewsets,
    permissions,
    response,
    status,
    serializers,
    decorators,
)
from api.support_classes import ReadOnlyOrAdmin, get_user_by_token
from django.shortcuts import get_object_or_404
from .serializer import CommentsSerializer
from blog.models import Blog
from .models import Comments


import logging

logger = logging.getLogger("api")


class CommentsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()

    def create(self, request, *args, **kwargs):
        user = get_user_by_token(request, raise_error=False)
        if user is not None:
            request.data["user"] = user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # user = Account.objects.first()
        # if "parent" in request.data:
        #     comment = get_object_or_404(Comments, pk=request.data["parent"])
        #     parent = comment.user
        #     message = Message(
        #         sender=user,
        #         title=f"Пользователь {request.user.username} ответил на ваш комментарий",
        #         HTMLText=f'Пользователь {request.user.username} ответил на ваш комментарий.<br/><a href="/blog/{request.data["blog"]}/">Ссылка на комментарий</a>',
        #     )
        #     message.save()
        #     parent.received_messages.add(message)
        #     parent.save()
        # message2 = Message(
        #     sender=user,
        #     title=f"Пользователь {request.user.username} ответил на ваш комментарий",
        #     HTMLText=f'Пользователь {request.user.username} ответил на ваш комментарий.<br/><a href="/blog/{request.data["blog"]}/">Ссылка на комментарий</a>',
        # )
        # message2.save()
        # user.received_messages.add(message2)
        # user.save()
        blog = Blog.objects.get(id=serializer.data["get_blog"])
        # context = {
        #     "user": user and user.username or "anonymus",
        #     "text": request.data["text"],
        # }
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            blog.get_comments, status=status.HTTP_201_CREATED, headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = get_user_by_token(request)
        if instance.user != user or not user.is_admin:
            raise serializers.ValidationError("У вас нет прав на это действие")

        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        user = get_user_by_token(request, raise_error=False)
        user = None
        if instance.user != user or not user.is_admin:
            raise serializers.ValidationError("У вас нет прав на это действие")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return response.Response(serializer.data)