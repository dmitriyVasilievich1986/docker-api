from comments.views import CommentsViewSet
from catalog.views import CatalogViewSet
from rest_framework import routers
from blog.views import BlogViewSet
from django.urls import path

router = routers.SimpleRouter()
router.register("blog", BlogViewSet)
router.register("catalog", CatalogViewSet)
router.register("comments", CommentsViewSet)

urlpatterns = router.urls