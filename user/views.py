from rest_framework import serializers
from django.http.response import JsonResponse
from django.shortcuts import render
from user.models import User
from os import environ
import requests
import json


def create_user_view(request, *args, **kwargs):
    host = environ.get("KNOX_AUTH_HOST", "http://localhost:8000/auth/accounts/")
    token = request.headers.get("Authorization", "")
    headers = {"Authorization": token}

    print(request.method)
    print(dir(request))

    r = requests.post(host, headers=headers, data={**request.data})
    if r.status_code >= 300:
        raise serializers.ValidationError(detail=r.text)
    user = User(**r.json())
    user.save()
    print(f"Create: {user}")
    return JsonResponse(r.json())
