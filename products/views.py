from django.db.models.query_utils import refs_expression
from products.serializers import (
    ProductSerializer,
)
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from products.permissions import IsOwnerOfProduct
from rest_framework.request import Request
from rest_framework.response import Response
from products.models import Product
from products.services import add_product, get_products, get_products_by_category
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated


class AddProductView(CreateAPIView):
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs):
        service = add_product
        print(request.data)
        status, context = service(request, self.serializer_class)
        return Response(status=status, data=context)


class GetProductsView(ListAPIView):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        service = get_products
        status, context = service(request, self.serializer_class)
        return Response(status=status, data=context)


class ProductSearchView(ListAPIView):
    # serializer_class =
    def get(self, request, *args, **kwargs):
        ...
        # return super().get(request, *args, **kwargs)


class DeleteProductView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOfProduct]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "product_id"


class UpdateProductView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOfProduct]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "product_id"


class GetProductsByCategoryView(ListAPIView):
    serializer_class = ProductSerializer

    def get(self, request, category_id):
        service = get_products_by_category
        status, context = service(
            request,
            self.serializer_class,
            category_id,
        )
        return Response(status=status, data=context)
