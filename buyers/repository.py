from buyers.models import BuyerSavedProduct, BuyerCart


class BuyerSavedProductRepo:
    not_found = BuyerSavedProduct.DoesNotExist
    model = BuyerSavedProduct.objects

    @classmethod
    def get_buyer_saved(cls, buyer):
        try:
            products = cls.model.get(buyer=buyer)
        except cls.not_found:
            return None
        else:
            return products

    @classmethod
    def create_buyer_saved(cls, **kwargs):
        saved = cls.model.create(**kwargs)
        return saved

    @classmethod
    def get_buyer_saved_products(cls, buyer):
        products = cls.model.filter(buyer=buyer)
        return products


class BuyerCartRepo:
    not_found = BuyerCart.DoesNotExist
    model = BuyerCart.objects

    @classmethod
    def get_buyer_cart(cls, buyer):
        try:
            products = cls.model.get(buyer=buyer)
        except cls.not_found:
            return None
        else:
            return products

    @classmethod
    def create_buyer_cart(cls, **kwargs):
        cart = cls.model.create(**kwargs)
        return cart

    @classmethod
    def get_buyer_cart_products(cls, buyer):
        products = cls.model.filter(buyer=buyer)
        return products
