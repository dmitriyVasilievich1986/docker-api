from django.db import models


class Catalog(models.Model):
    title = models.CharField(max_length=150, unique=False)
    name = models.CharField(max_length=150, unique=True)
    parent = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name="child",
        blank=True,
        null=True,
        to="self",
    )

    @property
    def _get_parameters(self, *args: list, **kwargs: dict) -> dict:
        return {"name": self.name, "title": self.title}

    @property
    def get_child(self, *args: list, **kwargs: dict) -> dict:
        payload: dict = {**self._get_parameters, "blog": list(), "catalog": list()}
        for blog in self.blog.all():
            payload["blog"].append(blog._get_parameters)
        for catalog in self.child.all():
            payload["catalog"].append(catalog.get_child)
        return payload

    @property
    def get_parent(self, *args: list, **kwargs: dict) -> dict:
        payload: list = [self._get_parameters]
        if self.parent is None:
            return payload
        payload += self.parent.get_parent
        return payload
