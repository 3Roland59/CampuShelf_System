from rest_framework.response import Response
from accounts.serializers import (
    UserCreationSerializer,
    CustomTokenObtainPairSerializer,
    UserSerializer,
    PhoneVericationSerializer,
    RequestPhoneVerificationSerializer,
    NotificationSerializer,
    RequestForgotPasswordSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
)
from accounts.utils import normalize_phone
from django.contrib.auth.hashers import check_password
from accounts.repository import (
    PhoneVerificationCodeRepo,
    NotificationRepository,
    UserRepository,
)
from utils.utils import send_sms_message, generate_code
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from accounts.services import (
    signup_service,
    request_password_reset_service,
    reset_password_service,
)
from django.utils import timezone
from rest_framework_simplejwt.views import TokenViewBase

# Create your views here.


class SignupView(CreateAPIView):
    serializer_class = UserCreationSerializer

    def post(self, request: Request, *args, **kwargs):
        service = signup_service
        status, context = service(request, self.serializer_class)
        return Response(status=status, data=context)


class UserDetailView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    user_repo = UserRepository
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        user = self.user_repo.get_user_by_id(request.user.pk)
        serializer = self.serializer_class(user, many=False)
        context = {
            "status": "success",
            "message": "user profile",
            "data": serializer.data,
        }
        return Response(status=status.HTTP_200_OK, data=context)

    def update(self, request: Request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            context = {
                "status": "success",
                "message": "User profile updated successfully.",
                "data": serializer.data,
            }
            return Response(status=status.HTTP_200_OK, data=context)
        else:
            context = {"status": "error", "message": serializer.errors}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenViewBase):
    serializer_class = CustomTokenObtainPairSerializer


class RequestPhoneNumberVerificationView(CreateAPIView):
    serializer_class = RequestPhoneVerificationSerializer
    repo = PhoneVerificationCodeRepo
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # phone = serializer.validated_data["phone"] # generate a interation error
            _phone = request.data.get("phone")
            # normalize phone number to able to send sms with mnotify
            phone = normalize_phone(_phone)
            code = generate_code(max=4, reset_password=True)
            self.repo.create_code(phone=_phone, code=code)
            send_sms_message(
                phone=phone,
                template="phone_verification.html",
                context={"code": code, "fname": "User"},
            )
            context = {
                "status": "success",
                "message": f"Verification code sent to {phone}.",
                "data": serializer.data,
            }
            return Response(status=status.HTTP_200_OK, data=context)


class PhoneVerifcationView(CreateAPIView):
    serializer_class = PhoneVericationSerializer
    repo = PhoneVerificationCodeRepo()
    user_repo = UserRepository()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"status": "failure", "message": "Invalid data.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        phone = request.data.get("phone")
        code = request.data.get("code")

        if not phone or not code:
            return Response(
                {"status": "failure", "message": "Phone and code are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        exists, v_code = self.repo.check_code(phone=phone)

        if not exists or not check_password(code, v_code.code):
            return Response(
                {"status": "failure", "message": "Phone number verification failed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if timezone.now() >= v_code.expires_in:
            v_code.delete()
            return Response(
                {"status": "failure", "message": "Verification code has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mark phone as verified
        v_code.delete()

        try:
            user = self.user_repo.get_user_by_phone(phone=phone)
            if user:
                user.phone_confirm = True
                user.save()
        except:
            pass

        return Response(
            {"status": "success", "message": "Phone number verified."},
            status=status.HTTP_200_OK
        )




class GetNotificationView(ListAPIView):
    serializer_class = NotificationSerializer
    repo = NotificationRepository
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_notifications = self.repo.get_unread_notifications(user=request.user)
        serializer = self.serializer_class(user_notifications, many=True)
        context = {"notifications": serializer.data}
        return Response(data=context, status=status.HTTP_200_OK)


class GetNotificationDetailView(ListAPIView):
    serializer_class = NotificationSerializer
    repo = NotificationRepository
    permission_classes = [IsAuthenticated]

    def get(self, request, notification_id):
        user_notification = self.repo.mark_as_read(notification_id=notification_id)
        serializer = self.serializer_class(user_notification)
        context = serializer.data
        return Response(data=context, status=status.HTTP_200_OK)


# for forgot password
class RequestForgotPasswordResetView(CreateAPIView):
    serializer_class = RequestForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        service = request_password_reset_service
        status, context = service(request, self.serializer_class)
        return Response(data=context, status=status)


# for forgot password
class ResetPasswordView(CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        service = reset_password_service
        status, context = service(request, self.serializer_class)
        return Response(data=context, status=status)


# """
#     this should not be confuse with reset password where the user does
#     not need to be authenticated and is assume to have forgotten
#     his/her password
#  """
class ChangePasswordView(CreateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_password = serializer.validated_data.get("new_password")
            user = request.user
            user.set_password(new_password)
            user.save()
            return Response(
                data={
                    "status": "success",
                    "message": "Password Change was successfull",
                },
                status=status.HTTP_200_OK,
            )
        return super().post(request, *args, **kwargs)
