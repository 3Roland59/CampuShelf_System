from django.urls import path
from reviews.views import ProductReviewCreateView, ContactUsCreateView

urlpatterns = [
    path(
        "review-product/",
        ProductReviewCreateView.as_view(),
        name="review-product",
    ),
    path("contact-us/", ContactUsCreateView.as_view(), name="contact-us-create"),
]
