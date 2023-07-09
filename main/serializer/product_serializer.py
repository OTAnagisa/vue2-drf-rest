from rest_framework import serializers

from main.models import ProductCategory, Product, Brand


class ProductCategorySerializer(serializers.ModelSerializer):
    """商品カテゴリ シリアライザ"""

    class Meta:
        model = ProductCategory
        fields = (
            "id",
            "name",
            "code",
            "order",
        )


class BrandSerializer(serializers.ModelSerializer):
    """商品カテゴリ シリアライザ"""

    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
        )


class ProductSerializer(serializers.ModelSerializer):
    """商品 シリアライザ"""

    category_name = serializers.CharField(source="category.name")
    category_id = serializers.UUIDField()
    amount = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()
    brand_id = serializers.SerializerMethodField()

    def get_amount(self, instance):
        amount = None
        if product_detail_all := instance.product_detail_all:
            amount = product_detail_all[0].amount
        return amount

    def get_brand_name(self, instance):
        brand_name = None
        if product_detail_all := instance.product_detail_all:
            brand_name = product_detail_all[0].brand.name
        return brand_name

    def get_brand_id(self, instance):
        brand_id = None
        if product_detail_all := instance.product_detail_all:
            brand_id = product_detail_all[0].brand_id
        return brand_id

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "no",
            "category_name",
            "category_id",
            "amount",
            "brand_name",
            "brand_id",
        )

