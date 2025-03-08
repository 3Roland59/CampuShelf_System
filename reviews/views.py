from rest_framework import generics
from reviews.models import ProductReview, ContactUs
from reviews.serializers import ProductReviewSerializer, ContactUsSerializer, ProductReviewCreateSerializer


class ProductReviewCreateView(generics.ListCreateAPIView):
    queryset = ProductReview.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductReviewCreateSerializer
        return ProductReviewSerializer


class ContactUsCreateView(generics.CreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
