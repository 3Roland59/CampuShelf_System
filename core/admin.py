from django.contrib import admin
from core.models import (
    ProductType,
    ProductCategory,
)
from django.utils.html import format_html

# Register your models here.


@admin.register(ProductCategory)
class Admin(admin.ModelAdmin):
    search_fields = ["category_name"]

    def _image(self, obj: ProductCategory):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
    list_display = ["category_name", "is_active", "_image"]


admin.site.register(ProductType)
