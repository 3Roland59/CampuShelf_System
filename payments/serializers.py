from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    UUIDField,
    IntegerField
)
from payments.models import ProductPayment
from products.serializers import ProductSerializer


class VerifyPaymentSerializer(ModelSerializer):

    class Meta:
        model = ProductPayment
        fields = [
            "product",
            "quantity",
            "reference",
            "transaction",
            "product_price_payed",
            "product_type",
            "number_of_days",
            "buyer",
        ]


class ListPaymentHistorySerializer(ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductPayment
        fields = (
            "product",
            "quantity",
            "reference",
            "product_price_payed",
            "product_type",
            "number_of_days",
            "payed_at",
            "payment_successful",
        )

        read_only_fields = [
            "reference",
        ]
