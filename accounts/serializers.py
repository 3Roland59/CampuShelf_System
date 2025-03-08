from typing import Any, Dict
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    BooleanField,
    ImageField,
    Serializer,
)
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth.models import update_last_login
from accounts.models import CustomUser, Notification
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings


class UserCreationSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "password",
        ]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.save()
        return user


class UserSerializer(ModelSerializer):
    phone_confirm = BooleanField(read_only=True)
    profile_image = ImageField()
    student_id_pic = ImageField()
    phone = PhoneNumberField()

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "profile_image",
            "phone_confirm",
            "location",
            "verified",
            "student_id",
            "student_id_pic",
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "phone": str(self.user.phone),
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "phone_confirm": self.user.phone_confirm,
            "location": self.user.location,
            "profile_image": (
                self.user.profile_image.url if self.user.profile_image else None
            ),
            "verified": self.user.verified,
            "student_id": self.user.student_id,
        }

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class RequestPhoneVerificationSerializer(Serializer):
    phone = PhoneNumberField()


class PhoneVericationSerializer(Serializer):
    phone = PhoneNumberField()
    code = CharField()


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class RequestForgotPasswordSerializer(Serializer):
    phone = PhoneNumberField()


class ResetPasswordSerializer(Serializer):
    phone = PhoneNumberField()
    code = CharField(max_length=5)
    new_password = CharField(max_length=255)


class ChangePasswordSerializer(Serializer):
    new_password = CharField(max_length=255)


