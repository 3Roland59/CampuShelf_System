from rest_framework.permissions import IsAuthenticated
from sellers.serializers import SellerProductSerializer
from sellers.services import get_user_products
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

# Create your views here.


class GetUserProductsView(RetrieveAPIView):
    serializer_class = SellerProductSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        status, context = get_user_products(request, self.serializer_class)
        return Response(status=status, data=context)
