from api.support_classes import (
    ReadOnlyOrAdmin,
    AuthenticatedUser,
    get_user_by_token,
)
from rest_framework import (
    viewsets,
    response,
    decorators,
    permissions,
    serializers,
    exceptions,
)
from django.contrib.postgres.search import SearchVector
from django.shortcuts import get_object_or_404
from .serializer import BlogSerializer
from user.models import User
from .models import Blog

# import logging

# logger = logging.getLogger("api")

PAGE_LENGTH = 5


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
    def by_name(self, request, pk=None, *args, **kwargs):
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
        if pk is None or not isinstance(pk, int):
            raise exceptions.NotFound()
        length = Blog.objects.count()
        start = max(0, pk * PAGE_LENGTH)
        end = min(length, pk * PAGE_LENGTH + PAGE_LENGTH)
        if start >= length:
            raise exceptions.NotFound()
        blog_reverse = Blog.objects.all()[::-1]
        blogs = [
            {
                "get_likes_count": x.get_likes_count,
                "get_view_count": x.get_view_count,
                "comments_count": x.comments_count,
                "title": x.title,
                "text": x.text,
                "name": x.name,
                "id": x.id,
            }
            for x in blog_reverse[start:end]
        ]
        result = {
            "blogs": blogs,
            "page": pk,
            "pages": length // PAGE_LENGTH,
        }
        return response.Response(result)
