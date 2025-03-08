from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    UUIDField,
    Serializer,
    IntegerField
)
from payments.models import ProductPayment
from products.serializers import ProductSerializer


class VerifyPaymentSerializer(Serializer):
    reference = CharField()
    transaction = CharField()
    product_id = UUIDField()
    quantity = IntegerField()


class ListPaymentHistorySerializer(ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductPayment
        fields = (
            "product",
            "quantity",
            "reference",
            "product_price_payed",
            "payed_at",
            "payment_successful",
        )

        read_only_fields = [
            "reference",
        ]
