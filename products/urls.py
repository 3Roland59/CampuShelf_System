from django.urls import path
from products.views import (
    GetProductsView,
    AddProductView,
    DeleteProductView,
    UpdateProductView,
    GetProductsByCategoryView,
)

app_name = "products"
urlpatterns = [
    path("all-products/", GetProductsView.as_view(), name="get-products"),
    path("add-product/", AddProductView.as_view(), name="add-product"),
    path(
        "<uuid:category_id>/",
        GetProductsByCategoryView.as_view(),
        name="category-products",
    ),
    path(
        "delete-product/<product_id>/",
        DeleteProductView.as_view(),
        name="delete-product",
    ),
    path(
        "update-product/<product_id>/",
        UpdateProductView.as_view(),
        name="update-product",
    ),
]
