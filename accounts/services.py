from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from utils.utils import generate_code
from accounts.repository import NotificationRepository, PhoneVerificationCodeRepo, UserRepository
from accounts.utils import normalize_phone
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from utils.utils import send_sms_message


def signup_service(request: Request, serializer_class):
    ok = HTTP_200_OK
    bad = HTTP_400_BAD_REQUEST
    notification_repo = NotificationRepository
    serializer = serializer_class(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data.get("email")
        first_name = serializer.validated_data.get("first_name")
        # phone = serializer.validated_data["phone"]
        _phone = request.data.get("phone")
        # context = {
        #     "first_name": first_name,
        #     "verification_code": generate_code(),
        # }
        user = serializer.save()
        
        notification_repo.create_verification_notification(user=user)

        phone = normalize_phone(_phone)
        send_sms_message(
            phone=phone,
            template="welcome.html",
            context={"fname": user.first_name},
        )
        context = {
            "status": "success",
            "message": "User added successfully, please verify your phone",
            "data": None,
        }
        return ok, context
    return bad, {"status": "failed", "message": "User was not added", "data": None}


def login_service(request: Request, serializer_class): ...


def request_password_reset_service(request: Request, serializer_class):
    bad = HTTP_400_BAD_REQUEST
    ok = HTTP_200_OK
    repo = PhoneVerificationCodeRepo
    user_repo = UserRepository
    serializer = serializer_class(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # phone = serializer.validated_data["phone"]
        _phone = request.data.get("phone")
        user = user_repo.get_user_by_phone(phone=_phone)
        if not user:
            context = {
                "status": "failed",
                "message": f"No user with phone {_phone}.",
                "data": None,
            }
            return (bad, context)
        # normalize phone number to able to send sms with mnotify
        phone = normalize_phone(str(_phone))
        code = generate_code(max=4, reset_password=True)
        repo.create_code(phone=_phone, code=code)
        send_sms_message(
            phone=phone,
            template="reset_password.html",
            context={"code": code, "fname": user.first_name},
        )
        context = {
            "status": "success",
            "message": f"Password reset code sent to {phone}.",
            "data": None,
        }
        return (ok, context)


def reset_password_service(request, serailizer_class):
    ok = HTTP_200_OK
    repo = PhoneVerificationCodeRepo
    bad = HTTP_400_BAD_REQUEST
    user_repo = UserRepository
    serailizer = serailizer_class(data=request.data)
    if serailizer.is_valid(raise_exception=True):
        phone = request.data.get("phone")
        code = request.data.get("code")
        new_password = request.data.get("new_password")
        exists, v_code = repo.check_code(phone=phone)
        if exists and check_password(code, v_code.code):
            if timezone.now() >= v_code.expires_in:
                context = {
                    "status": "failure",
                    "message": "Code has expired.",
                    "data": {"phone": phone},
                }
                v_code.delete()
                return bad, context
            context = {
                "status": "success",
                "message": "Password reset was successfull.",
                "data": {"phone": phone},
            }
            v_code.delete()
            try:
                # for if the user has not completed signup yet or phone does not exists
                user = user_repo.get_user_by_phone(phone=phone)
                user.set_password(new_password)
                user.save()
            except:
                pass
            return ok, context
        else:
            context = {
                "status": "failure",
                "message": "Code verification failed.",
                "data": {"phone": phone},
            }
            return bad, context
