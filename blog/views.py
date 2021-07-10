from api.support_classes import ReadOnlyOrAdmin, AllowAny
from django.contrib.postgres.search import SearchVector
from django.shortcuts import get_object_or_404
from .serializer import BlogSerializer
from .models import Blog

from rest_framework import (
    permissions,
    decorators,
    exceptions,
    response,
    viewsets,
)

import logging

logger: logging.Logger = logging.getLogger("api")


PAGE_LENGTH = 5


class BlogViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnlyOrAdmin]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def _get_blog(self, request, instance, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(instance)

        context = {
            **serializer.data,
            "is_liked": user in instance.likes.all(),
            "comments": instance.get_comments,
            "parent": instance.parent[1:][::-1],
        }

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
    def by_name(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(klass=Blog, name=pk)
        return self._get_blog(request, instance)

    @decorators.action(
        permission_classes=[AllowAny],
        methods=["POST"],
        detail=True,
    )
    def likes(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(klass=Blog, name=pk)
        user = request.user

        is_liked = user in instance.likes.all()
        instance.likes.remove(user) if is_liked else instance.likes.add(user)

        context = {
            "likes": instance.get_likes_count,
            "is_liked": not is_liked,
        }
        return response.Response(context)

    @decorators.action(
        permission_classes=[permissions.AllowAny],
        methods=["POST"],
        detail=False,
    )
    def search(self, request, *args, **kwargs):
        tags = request.data.get("tags", "")
        search_vector = SearchVector("text", config="russian")
        search = Blog.objects.annotate(search=search_vector).filter(search=tags)
        if search is None:
            raise exceptions.NotFound()
        result = [{"id": x.id, "name": x.name, "title": x.title} for x in search.all()]
        return response.Response(result)

    @decorators.action(
        permission_classes=[permissions.AllowAny],
        methods=["POST"],
        detail=False,
    )
    def page(self, request, *args, **kwargs):
        pk = request.data.get("page")
        page_length = request.data.get("page_length", PAGE_LENGTH)

        if pk is None or not isinstance(pk, int):
            raise exceptions.NotFound()

        length = Blog.objects.count()
        start = max(0, length - pk * page_length - page_length)
        end = min(length, length - pk * page_length)

        if start == end:
            raise exceptions.NotFound()

        blog_reverse = Blog.objects.all()[start:end][::-1]
        blogs = [self.get_serializer(x).data for x in blog_reverse]
        result = {
            "blogs": blogs,
            "page": pk,
            "page_length": page_length,
            "pages": length // page_length,
        }

        logger.debug(str(result))

        return response.Response(result)
