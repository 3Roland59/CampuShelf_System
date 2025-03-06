from django.db import models
from uuid import uuid4
from accounts.models import CustomUser
from products.models import Product

# Create your models here.


class ProductPayment(models.Model):
    payment_id = models.UUIDField(unique=True, primary_key=True, default=uuid4)
    reference = models.CharField(max_length=255, null=True, blank=True, editable=False)
    transaction = models.CharField("Transaction", max_length=50)
    quantity = models.IntegerField(default=1)
    buyer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="products_payments"
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True
    )
    product_price_payed = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name="Product price at the time of payment",
    )
    payed_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Payed")
    payment_successful = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Product Payment"
        verbose_name_plural = "Product Payments"

        db_table = "product_payment"

    def __str__(self):
        return str(self.buyer.email)
