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
