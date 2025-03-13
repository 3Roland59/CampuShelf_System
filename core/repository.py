from core.models import ProductType


class ProductTypeRepository:
    model = ProductType.objects
    not_found = ProductType.DoesNotExist

    @classmethod
    def get_type_by_id(cls, type_id):
        try:
            product_type = cls.model.get(id=type_id)
        except cls.not_found:
            return None
        else:
            return product_type
