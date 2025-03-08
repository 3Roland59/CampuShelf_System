from rest_framework.serializers import ModelSerializer
from buyers.models import BuyerSavedProduct, BuyerCart
from buyers.repository import BuyerSavedProductRepo, BuyerCartRepo
from products.serializers import ProductSerializer

buyer_sp_repo = BuyerSavedProductRepo
buyer_cart_repo = BuyerCartRepo


class BuyerSavedProductSerializer(ModelSerializer):
    class Meta:
        model = BuyerSavedProduct
        fields = ["saved_id", "products", "created_at", "last_updated"]
        read_only_fields = ["saved_id", "created_at", "last_updated"]

    def create(self, validated_data: dict):
        user = self.context.get("request").user
        validated_data.update({"buyer": user})
        products_data = validated_data.pop("products", [])

        buyer_saved = buyer_sp_repo.get_buyer_saved(buyer=user)

        if buyer_saved:
            for pd in products_data:
                buyer_saved.products.add(pd)
            return buyer_saved

        buyer_saved_product = buyer_sp_repo.create_buyer_saved(**validated_data)
        buyer_saved_product.products.set(products_data)
        return buyer_saved_product


class GetBuyerSavedProuductsSerializer(ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = BuyerSavedProduct
        fields = ["saved_id", "products", "created_at", "last_updated"]
        read_only_fields = [
            "saved_id",
            "created_at",
            "products",
            "last_updated",
        ]


class BuyerCartSerializer(ModelSerializer):
    class Meta:
        model = BuyerCart
        fields = ["cart_id", "products", "created_at", "last_updated"]
        read_only_fields = ["cart_id", "created_at", "last_updated"]

    def create(self, validated_data: dict):
        user = self.context.get("request").user
        validated_data.update({"buyer": user})
        products_data = validated_data.pop("products", [])

        buyer_cart = buyer_cart_repo.get_buyer_cart(buyer=user)

        if buyer_cart:
            for pd in products_data:
                buyer_cart.products.add(pd)
            return buyer_cart

        buyer_cart_product = buyer_cart_repo.create_buyer_cart(**validated_data)
        buyer_cart_product.products.set(products_data)
        return buyer_cart_product


class GetBuyerCartSerializer(ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = BuyerCart
        fields = ["cart_id", "products", "created_at", "last_updated"]
        read_only_fields = [
            "cart_id",
            "created_at",
            "products",
            "last_updated",
        ]
