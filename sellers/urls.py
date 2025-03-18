from django.urls import path
from sellers.views import (
    GetUserProductsView, GetUserBarterView,
)

urlpatterns = [
    path("user-products/", GetUserProductsView.as_view(), name="user-products"),
    path("user-barter-offers/", GetUserBarterView.as_view(), name="user-barter-offers"),
]
