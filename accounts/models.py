from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from uuid import uuid4

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not phone:
            raise ValueError("The Phone must be set")
        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(phone, email, password, **extra_fields)


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4)
    phone = PhoneNumberField(unique=True)
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_confirm = models.BooleanField(default=False)
    location = models.CharField(max_length=255, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile_images", null=True, blank=True)
    verified = models.BooleanField(default=False)
    student_id_pic = models.ImageField(upload_to="Student IDs", null=True, blank=True)
    student_id = models.CharField(max_length=255, null=True, blank=True, unique=True)

    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone", "first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"{self.email}"

    class Meta:
        db_table = "account"
        verbose_name = "Account"


class PhoneVerifcationCodes(models.Model):
    phone = PhoneNumberField()
    code = models.CharField(max_length=255)
    expires_in = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        verbose_name_plural = "PhoneVerificationCodes"

    def save(self, *args, **kwargs) -> None:
        self.expires_in = timezone.now() + timezone.timedelta(minutes=10)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.code)


status = [
    ("info", "info"),
    ("warning", "warning"),
]


class Notification(models.Model):
    notification_id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name="user",
        on_delete=models.CASCADE,
    )
    status = models.CharField(default="info", choices=status, max_length=50)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    opened = models.BooleanField(default=False)
