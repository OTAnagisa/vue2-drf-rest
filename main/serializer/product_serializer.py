from rest_framework import serializers

from main.models import ProductCategory, Product


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


class ProductSerializer(serializers.ModelSerializer):
    """商品 シリアライザ"""

    category_name = serializers.CharField(source="category.name")
    amount = serializers.SerializerMethodField()
    vendor_name = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()

    def get_amount(self, instance):
        amount = None
        if product_detail_all := instance.product_detail_all:
            amount = product_detail_all[0].amount
        return amount

    def get_vendor_name(self, instance):
        vendor_name = None
        if product_detail_all := instance.product_detail_all:
            vendor_name = product_detail_all[0].vendor.name
        return vendor_name

    def get_brand_name(self, instance):
        brand_name = None
        if product_detail_all := instance.product_detail_all:
            brand_name = product_detail_all[0].brand.name
        return brand_name

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "no",
            "category_name",
            "amount",
            "vendor_name",
            "brand_name",
        )

