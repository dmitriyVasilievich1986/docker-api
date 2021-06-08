from catalog.models import Catalog
from django.db import models
from user.models import User


class Blog(models.Model):
    title = models.CharField(max_length=150, unique=True)
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

    @property
    def get_view_count(self):
        return self.views.count()

    @property
    def get_comments(self):
        output = list()
        for comment in self.comments.all():
            output.append(comment.get_child)
        return output

    @property
    def comments_count(self):
        return sum([x.count for x in self.comments.all()]) if self.comments else 0
