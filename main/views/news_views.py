from rest_framework.generics import ListAPIView

from main.models import News
from main.serializer.news_serializer import NewsSerializer


class NewsListAPIView(ListAPIView):
    """投稿モデルの取得（一覧）APIクラス"""
    queryset = (
        News.objects.select_related("user", "category")
        .filter(is_deleted=False)
        .order_by("-publication_on", "category__order")
    )

    serializer_class = NewsSerializer
