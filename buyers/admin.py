from django.contrib import admin
from buyers.models import BuyerSavedProduct, BuyerCart

# Register your models here.


@admin.register(BuyerSavedProduct)
class Admin(admin.ModelAdmin):
    list_display = ["buyer", "saved_id"]

    fieldsets = (
        (
            "Buyer",
            {"fields": ("buyer",)},
        ),
        (
            "Saved",
            {"fields": ("products",)},
        ),
    )


class CartClassAdmin(admin.ModelAdmin):
    list_display = ["buyer", "cart_id"]

    fieldsets = (
        (
            "Buyer",
            {"fields": ("buyer",)},
        ),
        (
            "Cart",
            {"fields": ("products",)},
        ),
    )


admin.site.register(BuyerCart, CartClassAdmin)
