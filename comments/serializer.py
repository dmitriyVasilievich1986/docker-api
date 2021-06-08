from rest_framework import serializers
from .models import Comments


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = (
            "get_username",
            "get_child",
            "get_blog",
            "parent",
            "owner",
            "user",
            "text",
            "id",
        )
        read_only_fields = (
            "get_username",
            "get_child",
            "get_blog",
            "id",
        )
        extra_kwargs = {
            "parent": {"write_only": True},
            "owner": {"write_only": True},
            "user": {"write_only": True},
        }

    def update(self, instance, validated_data, *args, **kwargs):
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance