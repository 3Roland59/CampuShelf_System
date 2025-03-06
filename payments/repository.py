from payments.models import ProductPayment


class ProductPaymentRepository:
    model = ProductPayment.objects

    @classmethod
    def ceate_package_payment(
        cls,
        **kwargs
    ):
        product_payment = cls.model.create(
            **kwargs
                    )
        return product_payment
