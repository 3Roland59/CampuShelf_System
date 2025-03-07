from core.views import GetProductTypesView, GetProductCategoriesView
from django.urls import path

urlpatterns = [
    path("products-types/", GetProductTypesView.as_view(), name="types"),
    path("products-categories/", GetProductCategoriesView.as_view(), name="categories"),
]
