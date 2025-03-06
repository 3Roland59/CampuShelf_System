from django.db import models
from uuid import uuid4
from sellers.models import CustomUser
from core.models import ProductCategory, ProductType

# Create your models here.


class Product(models.Model):
    seller = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="seller_products"
    )
    product_id = models.UUIDField(
        primary_key=True, editable=False, unique=True, default=uuid4
    )
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, related_name="category_products"
    )
    description = models.TextField(max_length=255, null=True, blank=True)
    product_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    quantity = models.IntegerField(max_length=5, default=1)
    is_approved = models.BooleanField(default=True)
    product_type = models.ForeignKey(
        ProductType, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_posted = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self) -> str:
        return f"{self.product_name}"

    class Meta:
        db_table = "product"



class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images"
    )
    image = models.ImageField(upload_to="product_images")

    def __str__(self) -> str:
        return f"{self.product.product_id}"

    class Meta:
        db_table = "product_image"
