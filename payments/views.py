from rest_framework.permissions import IsAuthenticated
from payments.serializers import (
    ListPaymentHistorySerializer,
    VerifyPaymentSerializer,
)
from payments.services import verify_product_payment, get_user_payment
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from payments.models import ProductPayment


class ProductPaymentView(CreateAPIView):
    queryset = ProductPayment.objects.all()
    serializer_class = VerifyPaymentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        service = verify_product_payment
        status, context = service(request, self.serializer_class)
        return Response(status=status, data=context)


class PaymentHistoryView(ListAPIView):
    queryset = ProductPayment.objects.all()
    serializer_class = ListPaymentHistorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        status, context = get_user_payment(request, self.serializer_class)
        return Response(status=status, data=context)
