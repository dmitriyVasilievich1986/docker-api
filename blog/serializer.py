from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            "comments_count",
            "likes_count",
            "view_count",
            "created_at",
            "updated_at",
            "catalog",
            "title",
            "text",
            "name",
            "id",
        )
        read_only_fields = (
            "comments_count",
            "likes_count",
            "view_count",
            "updated_at",
            "created_at",
            "id",
        )

    def update(self, instance, validated_data, *args, **kwargs):
        instance.catalog = validated_data.get("catalog", instance.catalog)
        instance.title = validated_data.get("title", instance.title)
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance
