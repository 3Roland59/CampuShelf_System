from django.db import models
from uuid import uuid4

# Create your models here.

product_type = (
    ("barter", "Barter"),
    ("sale", "Sale"),
    ("rental", "Rental"),
)


class ProductCategory(models.Model):
    category_id = models.UUIDField(
        primary_key=True, unique=True, editable=False, default=uuid4
    )
    category_name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(
        upload_to="category_images",
        null=True,
        blank=True,
    )
    description = models.TextField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.category_name}"

    class Meta:
        db_table = "product_category"
        verbose_name_plural = "Product Categories"


class ProductType(models.Model):
    type_name = models.CharField(choices=product_type, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.type_name}"

    class Meta:
        db_table = "product_type"
        verbose_name_plural = "Product Types"
