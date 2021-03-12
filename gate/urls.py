from django.urls import path
from rest_framework import routers
from blog.views import BlogViewSet
from catalog.views import CatalogViewSet

router = routers.SimpleRouter()
router.register("blog", BlogViewSet)
router.register("catalog", CatalogViewSet)

urlpatterns = router.urls