from rest_framework import serializers

from main.models import User


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