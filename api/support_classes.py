from rest_framework import permissions
from rest_framework import exceptions
from user.models import User
from os import environ
import requests

import logging

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger("api")

class ReadOnlyOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        user = get_user_by_token(request, raise_error=False)
        request.user = user
        return request.method == "GET" or user and user.is_admin or False


class AuthenticatedUser(permissions.BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        user = get_user_by_token(request)
        request.user = user
        return user is not None

        
class AllowAny(permissions.BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        user = get_user_by_token(request)
        request.user = user
        return True


def get_user_by_token(request, raise_error=True):
    url_for_docker = "http://localhost:8000/auth/accounts/"
    host = environ.get("KNOX_AUTH_HOST", url_for_docker)
    token = request.headers.get("Authorization", "")
    headers = {"Authorization": token}

    r = requests.get(host, headers=headers)
    if r.status_code != 200:
        if raise_error:
            raise exceptions.PermissionDenied()
        return None

    return save_user(r.json())


def save_user(data):
    user = User(
        is_admin=data["is_superuser"],
        username=data["username"],
        id=data["id"],
    )
    user.save()
    return user
