from django.db import models
from user.models import User
from blog.models import Blog


class Comments(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True, null=True)

    user = models.ForeignKey(
        related_name="blog_comment",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        to=User,
    )
    owner = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name="comments",
        blank=True,
        null=True,
        to=Blog,
    )
    parent = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name="child",
        blank=True,
        null=True,
        to="self",
    )

    @property
    def get_blog(self, *args: list, **kwargs: dict) -> int:
        return self.owner.id if self.owner else self.parent.get_blog

    @property
    def _get_parameters(self, *args: list, **kwargs: dict) -> dict:
        return {"id": self.id, "user": self.get_username, "text": self.text}

    @property
    def get_child(self, *args: list, **kwargs: dict) -> dict:
        if self.child.count():
            payload: dict = {**self._get_parameters, "comments": list()}
            for comment in self.child.all():
                payload["comments"].append(comment.get_child)
            return payload
        return self._get_parameters

    @property
    def get_username(self, *args: list, **kwargs: dict) -> str:
        return self.user and self.user.username or "anonymus"

    @property
    def count(self, *args: list, **kwargs: dict) -> int:
        return 1 + sum([x.count for x in self.child.all()]) if self.child.count() else 1
