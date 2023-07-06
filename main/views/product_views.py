from django.db.models import Prefetch
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import ProductCategory, Product, ProductDetail
from main.serializer.product_serializer import ProductCategorySerializer, ProductSerializer


class ProductCategoryListAPIView(ListAPIView):
    """商品カテゴリー ListAPIView"""
    queryset = ProductCategory.objects.filter(is_deleted=False).order_by("order").only("name", "order", "code")
    serializer_class = ProductCategorySerializer


class ProductAPIView(APIView):
    """商品 APIView"""

    def get(self, request):
        params = request.query_params

        qs = (
            Product.objects.select_related("category")
            .prefetch_related(
                Prefetch(
                    "productdetail_set",
                    queryset=(
                        ProductDetail.objects.select_related("vendor", "brand")
                        .filter(is_deleted=False).only("amount", "product_id", "vendor__name", "brand__name")
                    ),
                    to_attr="product_detail_all"
                )
            )
            .filter(is_deleted=False)
        )
        if category_id := params.get("product_category_id"):
            qs = qs.filter(category_id=category_id)

        serializer = ProductSerializer(qs, many=True)

        return Response(serializer.data)

