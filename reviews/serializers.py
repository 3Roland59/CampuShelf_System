from rest_framework import serializers
from reviews.models import ProductReview, ContactUs
from accounts.serializers import UserSerializer
from accounts.models import CustomUser


# class ProductReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         user = UserSerializer()
#         model = ProductReview
#         fields = [
#             "user",
#             "product",
#             "review",
#             "rating",
#             "created_at",
#         ]


class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = ProductReview
        fields = [
            "user",
            "product",
            "review",
            "rating",
            "created_at",
        ]

    def get_user(self, obj):
        return UserSerializer(obj.user).data


class ProductReviewCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = ProductReview
        fields = ["user", "product", "review", "rating"]


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ["name", "email", "message"]
