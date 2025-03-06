from products.models import Product, ProductImage


class ProductRepository:
    not_found = Product.DoesNotExist
    model = Product.objects

    @classmethod
    def create_product(cls, **kwargs):
        product = cls.model.create(**kwargs)
        return product

    @classmethod
    def get_product_by_id(cls, product_id):
        try:
            product = cls.model.get(product_id=product_id)
        except cls.not_found:
            return None
        else:
            return product

    @classmethod
    def get_all_products(cls):
        return cls.model.all()

    @classmethod
    def get_all_products_by_category(cls, category_id):
        try:
            products = cls.model.get(category=category_id)
            return products
        except:
            return None

    @classmethod
    def get_user_products(cls, seller=None):
        products = cls.model.filter(seller=seller)
        return products


class ProductImageRepository:
    model = ProductImage

    @classmethod
    def create_product_image(cls, **kwargs):
        pdi = cls.model.objects.create(**kwargs)
        return pdi
