from django.contrib import admin
from accounts.models import CustomUser, PhoneVerifcationCodes, Notification
from django.utils.translation import gettext_lazy as _

# Register your models here.


class UserClassAdmin(admin.ModelAdmin):
    list_display = ["phone", "first_name", "email"]

    fieldsets = (
        ("Identity", {"fields": ("email",)}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "profile_image",
                    "location",
                    "student_id",
                    "student_id_pic",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "groups",
                    "user_permissions",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            _("Validation"),
            {
                "fields": (
                    "phone_confirm",
                    "verified",
                    )
            },
        ),
    )


class NotificationClassAdmin(admin.ModelAdmin):
    list_display = ["user", "status", "created_at"]


admin.site.register(CustomUser, UserClassAdmin)

admin.site.register(PhoneVerifcationCodes)

admin.site.register(Notification, NotificationClassAdmin)
