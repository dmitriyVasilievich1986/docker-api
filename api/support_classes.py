from rest_framework import permissions
from user.models import User
from os import environ
from django.shortcuts import get_object_or_404
from rest_framework import exceptions
import requests
import functools

# import logging

# logger = logging.getLogger("api")


class ReadOnlyOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        if request.method == "GET":
            return True

        user = get_user_by_token(request, raise_error=False)
        return user and user.is_admin or False


class AuthenticatedUser(permissions.BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        user = get_user_by_token(request)
        return True


def get_user_by_token(request, raise_error=True):
    host = environ.get("KNOX_AUTH_HOST", "http://localhost:8000/auth/accounts/")
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
