from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            "id",
            "name",
            "text",
            "title",
            "created_at",
            "updated_at",
            "comments_count",
            "get_view_count",
            "get_likes_count",
        )
        read_only_fields = (
            "id",
            "created_at",
            "comments_count",
            "get_view_count",
            "get_likes_count",
        )

    def update(self, instance, validated_data, *args, **kwargs):
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.title = validated_data.get("title", instance.title)
        instance.catalog = validated_data.get("catalog", instance.catalog)
        instance.save()
        return instance