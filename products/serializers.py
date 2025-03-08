from rest_framework.serializers import ModelSerializer
from products.models import Product, ProductImage
from accounts.serializers import UserSerializer
from products.repository import ProductRepository
from core.serializers import ProductCategorySerializer, ProductTypeSerializer

product_repo = ProductRepository


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image",)


class ProductSerializer(ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    seller = UserSerializer(read_only=True)
    category = ProductCategorySerializer()
    product_type = ProductTypeSerializer()

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
            "is_approved",
            "date_posted",
            "last_updated",
            "product_images",
        ]

    def create(self, validated_data: dict):
        product = product_repo.create_product(**validated_data)
        return product

    def update(self, instance, validated_data):
        # images_data = validated_data.pop("images", [])

        # Update the product fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update images
        # instance.product_images.all().delete()  # Clear existing images

        # for image_data in images_data:
        # ProductImage.objects.create(product=instance, **image_data)

        return instance
