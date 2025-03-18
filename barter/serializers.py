from barter.models import Barter
# from accounts.serializers import UserSerializer
from rest_framework.serializers import ModelSerializer, ImageField
from products.serializers import ProductSerializer


class BarterSerializer(ModelSerializer):
    # seller = UserSerializer(read_only=True)
    product = ProductSerializer()
    barter_image = ImageField()

    class Meta:
        model = Barter
        fields = [
            "barter_id",
            "seller",
            "barter_name",
            "buyer",
            "description",
            "barter_image",
            "product",
            "date_posted",
            "last_updated",
        ]


class BarterCreateSerializer(ModelSerializer):

    class Meta:
        model = Barter
        fields = [
            "seller",
            "barter_name",
            "buyer",
            "description",
            "barter_image",
            "product",
        ]
