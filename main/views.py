from django.db.models import Prefetch
from rest_framework import generics, views
from rest_framework.response import Response

from main.models import News, User, AffiliationHistory
from main.serializer import NewsSerializer, UserListSerializer


class NewsListAPIView(generics.ListAPIView):
    """投稿モデルの取得（一覧）APIクラス"""
    queryset = (
        News.objects.select_related("user", "category")
        .filter(is_deleted=False)
        .order_by("-publication_on", "category__order")
    )

    serializer_class = NewsSerializer


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

