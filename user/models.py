from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, blank=True, null=True)
    is_admin = models.BooleanField(default=False)