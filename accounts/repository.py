from accounts.models import CustomUser, PhoneVerifcationCodes, Notification
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist


class UserRepository:
    model = CustomUser.objects

    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.model.filter(id=user_id).first()

    @classmethod
    def get_user_by_email(cls, email):
        return cls.model.filter(email=email).first()

    @classmethod
    def get_user_by_phone(cls, phone):
        return cls.model.filter(phone=phone).first()

    @classmethod
    def create_user(cls, **kwargs):
        user = cls(**kwargs)
        user.save()
        return user

    @classmethod
    def update_user(cls, user_id, **kwargs):
        user = cls.get_user_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            user.save()
        return user

    @classmethod
    def delete_user(cls, user_id):
        user = cls.get_user_by_id(user_id)
        if user:
            user.delete()
            return True
        return False

    @classmethod
    def verify_user(cls, user_id):
        user = cls.get_user_by_id(user_id)
        if user:
            user.verified = True
            user.save()
            return True
        return False




class PhoneVerificationCodeRepo:
    model = PhoneVerifcationCodes.objects

    @classmethod
    def create_code(cls, phone, code):
        _code = make_password(code)
        if cls.model.filter(phone=phone).exists():
            cls.model.get(phone=phone).delete()
        cls.model.create(phone=phone, code=_code)

    @classmethod
    def check_code(cls, phone):
        try:
            v_code = cls.model.get(phone=phone)
            return True, v_code
        except:
            return False, None


class NotificationRepository:
    model = Notification.objects

    @classmethod
    def get_notification_by_id(cls, notification_id):
        try:
            notification = cls.model.get(id=notification_id)
        except ObjectDoesNotExist:
            return None
        else:
            return notification

    @classmethod
    def get_notifications_by_user(cls, user):
        notifications = cls.model.filter(user=user)
        return notifications

    @classmethod
    def get_unread_notifications(cls, user):
        unread_notifications = cls.model.filter(user=user, opened=False)
        return unread_notifications

    @classmethod
    def mark_as_read(cls, notification_id):
        try:
            notification = cls.model.get(pk=notification_id)
            notification.opened = True
            notification.save()
        except ObjectDoesNotExist:
            return {}
        else:
            return notification

    @classmethod
    def create_notification(cls, user, subject, message, status):
        notification = cls.model.create(
            user=user,
            subject=subject,
            message=message,
            status=status,
        )
        return notification

    @classmethod
    def create_verification_notification(cls, user):
        subject = "Account Verification Needed"
        message = (
            "Thank you for registering! Please verify your phone number to verify your account. "
            "Check your inbox for a verification code, and follow the instructions to complete the process."
        )
        status = "warning"
        notification = cls.create_notification(user, subject, message, status)
        return notification
