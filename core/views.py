from rest_framework.generics import ListAPIView
from core.serializers import (
    ProductTypeSerializer,
    ProductCategorySerializer,
)

from core.models import ProductType, ProductCategory
# Create your views here.


class GetProductTypesView(ListAPIView):
    serializer_class = ProductTypeSerializer

    def get_queryset(self):
        queryset = ProductType.objects.filter(
            is_active=True,
        ).all()
        return queryset


class GetProductCategoriesView(ListAPIView):
    serializer_class = ProductCategorySerializer

    def get_queryset(self):
        queryset = ProductCategory.objects.filter(
            is_active=True,
        ).all()
        return queryset
