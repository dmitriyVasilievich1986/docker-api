from django.urls import path, include
from user.views import create_user_view

urlpatterns = [
    path("api/", include("gate.urls")),
    path("api/create_user/", create_user_view, name="create_user"),
]
