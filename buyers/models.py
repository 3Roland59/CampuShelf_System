from django.db import models
from uuid import uuid4
from ..accounts.models import CustomUser
from ..products.models import Product
# Createyour models here.


class BuyerSavedProduct(models.Model):
    buyer = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    saved_id = models.UUIDField(primary_key=True, default=uuid4, unique=True)
    products = models.ManyToManyField(to=Product)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "buyer_saved_products"
        verbose_name = "Buyer Saved Product"
        verbose_name_plural = "Buyer Saved Products"

    def __str__(self):
        return str(self.buyer.email)


class BuyerCart(models.Model):
    buyer = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cart_id = models.UUIDField(primary_key=True, default=uuid4, unique=True)
    products = models.ManyToManyField(to=Product)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "buyer_cart"
        verbose_name = "Buyer Cart"

    def __str__(self):
        return str(self.buyer.email)
