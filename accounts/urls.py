from django.urls import path
from accounts.views import (
    SignupView,
    LoginView,
    UserDetailView,
    RequestPhoneNumberVerificationView,
    PhoneVerifcationView,
    GetNotificationView,
    ResetPasswordView,
    RequestForgotPasswordResetView,
    GetNotificationDetailView,
    ChangePasswordView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", SignupView.as_view(), name="signup"),
    path(
        "request-sms-verification/",
        RequestPhoneNumberVerificationView.as_view(),
        name="request-sms",
    ),
    path(
        "verify-phone/", PhoneVerifcationView.as_view(), name="phone-verification"
    ),
    path("user-profile/", UserDetailView.as_view(), name="user-profile"),
    path("login/", LoginView.as_view(), name="obtain-token"),
    # use for forgot password
    path(
        "request-forgot-password/",
        RequestForgotPasswordResetView.as_view(),
        name="request-password-reset",
    ),
    # use for forgot password
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    # change password
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path(
        "get-user-notifications/", GetNotificationView.as_view(), name="notifications"
    ),
    path(
        "get-user-notifications/<uuid:notification_id>/",
        GetNotificationDetailView.as_view(),
        name="notifications",
    ),
]
