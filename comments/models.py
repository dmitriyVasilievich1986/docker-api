from django.db import models
from user.models import User
from blog.models import Blog


class Comments(models.Model):
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
    def get_blog(self):
        if self.owner is not None:
            return self.owner.id
        return self.parent.get_blog

    @property
    def get_child(self):
        if not self.child.count():
            return {"id": self.id, "user": self.get_username, "text": self.text}
        output = {
            "user": self.get_username,
            "text": self.text,
            "id": self.id,
            "child": list(),
        }
        for child in self.child.all():
            output["child"].append(child.get_child)
        return output

    @property
    def get_username(self):
        return self.user and self.user.username or "anonymus"

    @property
    def count(self):
        return 1 + sum([x.count for x in self.child.all()]) if self.child.count() else 1