from rest_framework.permissions import IsAuthenticated
from sellers.serializers import SellerProductSerializer, SellerBarterSerializer
from sellers.services import get_user_products, get_user_barter
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

# Create your views here.


class GetUserProductsView(RetrieveAPIView):
    serializer_class = SellerProductSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        status, context = get_user_products(request, self.serializer_class)
        return Response(status=status, data=context)


class GetUserBarterView(RetrieveAPIView):
    serializer_class = SellerBarterSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        status, context = get_user_barter(request, self.serializer_class)
        return Response(status=status, data=context)
