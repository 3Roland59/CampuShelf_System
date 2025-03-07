from rest_framework.serializers import ModelSerializer
from core.models import ProductCategory, ProductType


class ProductTypeSerializer(ModelSerializer):
    class Meta:
        model = ProductType
        fields = "__all__"


class ProductCategorySerializer(ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = "__all__"
