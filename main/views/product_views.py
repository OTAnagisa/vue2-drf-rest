from django.db.models import Prefetch
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from main.common.util import Bulk
from main.models import ProductCategory, Product, ProductDetail, Brand
from main.serializer.product_serializer import ProductCategorySerializer, ProductSerializer, BrandSerializer


class ProductCategoryListAPIView(ListAPIView):
    """商品カテゴリー ListAPIView"""
    queryset = ProductCategory.objects.filter(is_deleted=False).order_by("order").only("name", "order", "code")
    serializer_class = ProductCategorySerializer


class BrandListAPIView(ListAPIView):
    """商品カテゴリー ListAPIView"""
    queryset = Brand.objects.filter(is_deleted=False).order_by("no").only("name")
    serializer_class = BrandSerializer


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
                        ProductDetail.objects.select_related("brand")
                        .filter(is_deleted=False).only("amount", "product_id", "brand__name")
                    ),
                    to_attr="product_detail_all"
                )
            )
            .filter(is_deleted=False)
            .order_by("no")
            .only("name", "no", "category__name")
        )

        if product_name := params.get("product_name"):
            qs = qs.filter(name__contains=product_name)

        if category_id := params.get("product_category_id"):
            qs = qs.filter(category_id=category_id)

        if brand_id := params.get("brand_id"):
            qs = qs.filter(productdetail__brand_id=brand_id)

        serializer = ProductSerializer(qs, many=True)

        return Response(serializer.data)

    def post(self, request):
        """保存処理"""
        request_data = request.data
        # 変更のあった商品
        changed_product_dict = request_data["changed_product_dict"]
        # 削除する商品
        delete_product_id_list = request_data["delete_product_id_list"]
        self.update_product(changed_product_dict, delete_product_id_list)
        self.update_product_detail(changed_product_dict, delete_product_id_list)

        return Response(status=HTTP_200_OK)

    @classmethod
    def update_product(cls, changed_product_dict, delete_product_id_list):
        """商品アップデート"""
        product_id_list = [*changed_product_dict.keys(), *delete_product_id_list]
        # 対象の商品を取得
        product_qs = Product.objects.filter(id__in=product_id_list)

        update_product_list = []
        for product in product_qs:
            product_id = str(product.id)
            # 更新
            if change_data := changed_product_dict.get(product_id):
                product.name = change_data["name"]
                product.category_id = change_data["category_id"]

            # 論理削除
            if product_id in delete_product_id_list:
                product.is_deleted = True

            update_product_list.append(product)

        # 一括保存
        Bulk.update(Product, update_product_list, fields=["name", "category_id", "is_deleted"])

    @classmethod
    def update_product_detail(cls, changed_product_dict, delete_product_id_list):
        """商品詳細アップデート"""
        product_id_list = [*changed_product_dict.keys(), *delete_product_id_list]
        # 対象の商品詳細を取得
        product_detail_qs = ProductDetail.objects.filter(product_id__in=product_id_list)

        update_product_list = []
        for product_detail in product_detail_qs:
            product_id = str(product_detail.product_id)
            # 更新
            if change_data := changed_product_dict.get(product_id):
                product_detail.amount = change_data["amount"]
                product_detail.brand_id = change_data["brand_id"]

            # 論理削除
            if product_id in delete_product_id_list:
                product_detail.is_deleted = True

            update_product_list.append(product_detail)

        # 一括保存
        Bulk.update(ProductDetail, product_detail_qs, fields=["amount", "brand_id", "is_deleted"])
