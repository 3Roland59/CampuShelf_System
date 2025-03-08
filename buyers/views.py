from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView, DestroyAPIView
from buyers.serializers import (
    BuyerSavedProductSerializer,
    GetBuyerSavedProuductsSerializer,
    BuyerCartSerializer,
    GetBuyerCartSerializer,
)
from buyers.services import get_buyer_saved_products, delete_saved_product, get_buyer_cart_products, delete_cart_product
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class SaveProductView(CreateAPIView):
    serializer_class = BuyerSavedProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RemoveSavedProductView(DestroyAPIView):
    """
    Removing saved products from saved
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        service = delete_saved_product
        status, context = service(request, product_id=product_id)
        return Response(status=status, data=context)


class GetBuyerSaveProductView(GenericAPIView):
    serializer_class = GetBuyerSavedProuductsSerializer
    permission_classes = [IsAuthenticated]
    # for browser testing
    # authentication_classes = [SessionAuthentication]

    def get(self, request, *args, **kwargs):
        # serive should be in the function scope
        # to vaoid class state errors
        service = get_buyer_saved_products
        status, context = service(request, self.serializer_class)
        return Response(status=status, data=context)


class CartView(CreateAPIView):
    serializer_class = BuyerCartSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RemoveCartView(DestroyAPIView):
    """
    Removing products from cart
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        service = delete_cart_product
        status, context = service(request, product_id=product_id)
        return Response(status=status, data=context)


class GetBuyerCartView(GenericAPIView):
    serializer_class = GetBuyerCartSerializer
    permission_classes = [IsAuthenticated]
    # for browser testing
    # authentication_classes = [SessionAuthentication]

    def get(self, request, *args, **kwargs):
        # serive should be in the function scope
        # to vaoid class state errors
        service = get_buyer_cart_products
        status, context = service(request, self.serializer_class)
        return Response(status=status, data=context)
