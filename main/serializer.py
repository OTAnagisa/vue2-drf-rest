from rest_framework import serializers

from main.models import News, User


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


class UserListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="full_name")
    department_section_name = serializers.SerializerMethodField()

    def get_department_section_name(self, instance):
        affiliation_history = instance.affiliation_history
        if not affiliation_history:
            return ""
        section = affiliation_history[0].section
        department = section.department

        return f"{department.name}{section.name}"

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "department_section_name",
        )
