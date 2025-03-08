from django.contrib import admin
from payments.models import ProductPayment

# Register your models here.


@admin.register(ProductPayment)
class ProductPaymentAdmin(admin.ModelAdmin):
    list_display = [
        "buyer",
        "product",
        "quantity",
        "product_price_payed",
        "payment_successful",
    ]
