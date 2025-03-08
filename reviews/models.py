from django.db import models
from products.models import Product
from accounts.models import CustomUser

# Create your models here.


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    review = models.TextField()
    created_at = models.DateTimeField(
        verbose_name="reported on", auto_now=False, auto_now_add=True
    )
    rating = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Product Review"


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(verbose_name="Sent on", auto_now_add=True)

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"
