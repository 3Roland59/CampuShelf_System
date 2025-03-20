from rest_framework.serializers import ModelSerializer, ImageField
# from core.serializers import ProductTypeSerializer, ProductCategorySerializer
from products.models import Product
from products.serializers import ProductImageSerializer
from barter.models import Barter
from accounts.serializers import UserSerializer
# from products.serializers import ProductSerializer


class SellerProductSerializer(ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    seller = UserSerializer(read_only=True)
    # category = ProductCategorySerializer()
    # product_type = ProductTypeSerializer()

    class Meta:
        model = Product
        fields = [
            "product_id",
            "seller",
            "product_name",
            "category",
            "product_type",
            "quantity",
            "description",
            "product_price",
            "old_price",
            "is_approved",
            "date_posted",
            "last_updated",
            "product_images",
        ]


class SellerBarterSerializer(ModelSerializer):
    buyer = UserSerializer(read_only=True)
    # product = ProductSerializer()
    barter_image = ImageField()

    class Meta:
        model = Barter
        fields = [
            "barter_id",
            "seller",
            "barter_name",
            "buyer",
            "description",
            "barter_image",
            "product",
            "date_posted",
            "last_updated",
        ]
