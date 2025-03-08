from django.urls import path
from payments.views import (
    ProductPaymentView,
    PaymentHistoryView,
)

urlpatterns = [
    path("product-payment/", ProductPaymentView.as_view(), name="product-payment"),
    path(
        "product-payment-history/",
        PaymentHistoryView.as_view(),
        name="product-payment-history",
    ),
]
