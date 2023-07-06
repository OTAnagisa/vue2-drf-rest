from django.db.models import Prefetch
from rest_framework import generics, views
from rest_framework.response import Response

from main.models import AffiliationHistory, User
from main.serializer.user_serializer import UserListSerializer


class UserListAPIView(views.APIView):
    """ユーザー一覧取得API"""
    def get(self, request):
        ah_qs = (
            AffiliationHistory.objects.current(includes_retired_last=True)
            .select_related("section__department")
            .only(
                "user_id",
                "section__name",
                "section__department__name",
            )
        )
        u_qs = (
            User.objects.prefetch_related(
                Prefetch(
                    "affiliationhistory_set",
                    queryset=ah_qs,
                    to_attr="affiliation_history"
                )
            ).filter(is_deleted=False)
            .only(
                "last_name",
                "first_name",
                "email",
            )
        )
        serializer = UserListSerializer(u_qs, many=True)
        return Response(serializer.data)
