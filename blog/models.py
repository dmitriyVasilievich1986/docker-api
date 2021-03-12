from django.db import models
from django.contrib.auth.models import User
from catalog.models import Catalog


class Blog(models.Model):
    title = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150, unique=True)
    created_at = models.DateField(auto_now_add=True)
    text = models.TextField(blank=True, null=True)
    updated_at = models.DateField(auto_now=True)
    likes = models.ManyToManyField(to=User)

    catalog = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name="blog",
        to=Catalog,
        blank=True,
        null=True,
    )