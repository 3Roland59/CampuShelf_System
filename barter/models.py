from django.db import models
from uuid import uuid4
from products.models import Product
from accounts.models import CustomUser
from cloudinary.models import CloudinaryField

# Create your models here.


class Barter(models.Model):
    barter_id = models.UUIDField(unique=True, primary_key=True, default=uuid4)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    barter_name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, null=True, blank=True)
    barter_image = CloudinaryField("barter_images")
    buyer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="buyer"
    )
    seller = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="seller"
    )
    date_posted = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
