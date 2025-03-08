from django.urls import path
from buyers.views import (
    SaveProductView,
    GetBuyerSaveProductView,
    RemoveSavedProductView,
    CartView,
    GetBuyerCartView,
    RemoveCartView,
)

urlpatterns = [
    path("save-product/", SaveProductView.as_view(), name="save-product"),
    path(
        "saved-products/remove/<uuid:product_id>/",
        RemoveSavedProductView.as_view(),
        name="remove-saved-product",
    ),
    path(
        "buyer-saved-products/",
        GetBuyerSaveProductView.as_view(),
        name="get-buyer-saved-products",
    ),
    path("cart/", CartView.as_view(), name="cart"),
    path(
        "cart/remove/<uuid:product_id>/",
        RemoveCartView.as_view(),
        name="remove-cart-product",
    ),
    path(
        "buyer-cart/",
        GetBuyerCartView.as_view(),
        name="get-buyer-cart",
    ),

]
