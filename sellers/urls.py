from django.urls import path
from sellers.views import (
    GetUserProductsView,
)

urlpatterns = [
    path("user-products/", GetUserProductsView.as_view(), name="user-products"),
]
