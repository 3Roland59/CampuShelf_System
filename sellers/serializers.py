from rest_framework.serializers import ModelSerializer
from core.serializers import ProductTypeSerializer, ProductCategorySerializer
from products.models import Product
from products.serializers import ProductImageSerializer


class SellerProductSerializer(ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    category = ProductCategorySerializer()
    product_type = ProductTypeSerializer()

    class Meta:
        model = Product
        fields = [
            "product_id",
            "product_name",
            "category",
            "product_type",
            "quantity",
            "description",
            "product_price",
            "is_approved",
            "date_posted",
            "last_updated",
            "product_images",
        ]
