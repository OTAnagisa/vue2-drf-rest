from rest_framework import serializers

from main.models import News


class NewsSerializer(serializers.ModelSerializer):
    """ニュース シリアライザ"""
    user_name = serializers.CharField(source="user.full_name")
    category_name = serializers.CharField(source="category.name")
    category_id = serializers.UUIDField()

    class Meta:
        model = News
        fields = (
            "title",
            "contents",
            "publication_on",
            "user_name",
            "category_name",
            "category_id",
        )
