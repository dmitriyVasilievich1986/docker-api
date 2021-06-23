from os import stat
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Blog
import requests
import json

class BlogTest(APITestCase):
    def get_user(self):
        data = {
            "username": "root",
            "password": "root",
        }
        r = requests.post('http://auth:8000/auth/accounts/login/', data=data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        token = r.json()['token']
        self.headers = {'Authorization': f'token {token}'}

    def test_create_blog(self):
        self.get_user()
        print(f'headers: {self.headers}')
        data = {
            "name": "test_blog",
            "title": "test_blog",
            "text": "some test text",
        }
        r = self.client.post('/api/blog/', data=data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        # r = self.client.post('/api/blog/', data=data, headers=self.headers)
        # self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_read_blog(self):
        r = self.client.get('/api/blog/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(Blog.objects.count(), 0)
