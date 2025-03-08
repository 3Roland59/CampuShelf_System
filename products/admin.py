from django.contrib import admin
from products.models import Product, ProductImage
from django.utils.html import format_html

# Register your models here.


@admin.register(ProductImage)
class ProductImagesAdmin(admin.ModelAdmin):

    def _image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
    list_display = ["_image", "product", "pk"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = [
        "is_approved",
    ]

    def image(self, obj: Product):
        product_image = obj.product_images.all().first()
        if product_image:
            return format_html('<img src="{}" width="50" height="50" />', product_image.image.url)
        else:
            return format_html('<span style="color: red;">&#x1F4C4;</span>')# 📄
    search_fields = ["product_name"]
    list_display = ["product_name", "seller", "category", "product_type", "quantity", "is_approved", "image"]
