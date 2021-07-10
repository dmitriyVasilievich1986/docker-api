from catalog.models import Catalog
from django.db import models
from user.models import User


class Blog(models.Model):
    title = models.CharField(max_length=150, unique=False)
    name = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True, null=True)

    likes = models.ManyToManyField(to=User, related_name="likes")
    views = models.ManyToManyField(to=User, related_name="views")

    catalog = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name="blog",
        to=Catalog,
        blank=True,
        null=True,
    )

    @property
    def _get_parameters(self, *args: list, **kwargs: dict) -> dict:
        return {"name": self.name, "title": self.title}

    @property
    def parent(self, *args: list, **kwargs: dict) -> list:
        payload: list = [self._get_parameters]
        if self.catalog is None:
            return payload
        payload += self.catalog.get_parent
        return payload

    @property
    def likes_count(self, *args: list, **kwargs: dict) -> int:
        return self.likes.count()

    @property
    def view_count(self, *args: list, **kwargs: dict) -> int:
        return self.views.count()

    @property
    def get_comments(self, *args: list, **kwargs: dict) -> list:
        payload = list()
        for comment in self.comments.all():
            payload.append(comment.get_child)
        return payload

    @property
    def comments_count(self):
        return sum([x.count for x in self.comments.all()]) if self.comments else 0
