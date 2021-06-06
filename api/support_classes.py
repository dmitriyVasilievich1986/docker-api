from rest_framework import permissions
from os import environ
import requests


class ReadOnlyOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        if request.method == "GET":
            return True

        r = get_user_from_by_code(request)
        return r.status_code == 200 and r.json().get("is_superuser", False) or False


class AuthenticatedUser(permissions.BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        r = get_user_from_by_code(request)
        return r.status_code == 200 and r.json().get("is_active", False) or False


def get_user_from_by_code(request):
    host = environ.get("KNOX_AUTH_HOST", "http://localhost:8000/auth/accounts/")
    token = request.headers.get("Authorization", "")
    headers = {"Authorization": token}

    r = requests.get(host, headers=headers)
    return r