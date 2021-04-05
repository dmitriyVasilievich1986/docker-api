from django.db import models


class Catalog(models.Model):
    title = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150, unique=True)
    parent = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name="child",
        blank=True,
        null=True,
        to="self",
    )

    @property
    def _get_parameters(self, *args, **kwargs):
        return {"name": self.name, "title": self.title}

    @property
    def get_child(self, *args, **kwargs):
        if self.child.all().count() == 0:
            blogs = list()
            for blog in self.blog.all():
                blogs.append({"name": blog.name, "title": blog.title})
            return {"name": self.name, "title": self.title, "blog": blogs}
        payload = {"name": self.name, "title": self.title, "child": list()}
        for child in self.child.all():
            payload["child"].append(child.get_child)
        return payload

    @property
    def get_parent(self, *args, **kwargs):
        if self.parent is None:
            return [{"name": self.name, "title": self.title}]
        payload = [
            {
                "name": self.name,
                "title": self.title,
            }
        ] + self.parent.get_parent
        return payload
