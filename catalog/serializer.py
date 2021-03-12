from rest_framework import serializers
from .models import Catalog


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = (
            "name",
            "title",
        )

    def update(self, instance, validated_data):
        instance.parent = validated_data.get("parent", instance.parent)
        instance.title = validated_data.get("title", instance.title)
        instance.name = validated_data.get("name", instance.name)
        instance.blog = validated_data.get("blog", instance.blog)
        instance.save()
        return instance