from django.contrib import admin
from .models import ProductReview, ContactUs


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "review", "created_at", "rating"]
    list_filter = ["created_at"]
    search_fields = ["product__name"]

    ordering = ["-created_at"]


admin.site.register(ProductReview, ProductReviewAdmin)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "message"]
    search_fields = ["name", "email"]
    list_filter = ["created_at"]

    ordering = ["name"]


admin.site.register(ContactUs, ContactUsAdmin)
