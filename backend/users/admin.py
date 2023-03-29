from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from recipes.admin import BaseReadOnlyAdmin
from .models import Subscription, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Админка для управления пользователями."""

    list_display = (
        "pk",
        "username",
        "email",
        "role",
        "is_active",
        "is_blocked",
    )
    list_editable = ("is_blocked",)
    search_fields = ("username", "email")

    fieldsets = (
        (_("Password"), {"fields": ("password",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_blocked",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            _("New user"),
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "email",
                ),
            },
        ),
    )

    superuser_fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "role",
                    "is_blocked",
                ),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self.add_fieldsets
        if request.user.is_superuser:
            return self.superuser_fieldsets
        return self.fieldsets


@admin.register(Subscription)
class SubscriptionAdmin(BaseReadOnlyAdmin):
    list_display = (
        "pk",
        "user",
        "author"
    )


admin.site.unregister(Group)
