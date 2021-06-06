from catalog.models import Catalog
from django.db import models
from user.models import User


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

    @property
    def get_parent(self, *args, **kwargs):
        if self.catalog is None:
            return [{"name": self.name, "title": self.title}]
        payload = [
            {
                "name": self.name,
                "title": self.title,
            }
        ] + self.catalog.get_parent
        return payload

    @property
    def get_likes_count(self):
        return self.likes.count()
