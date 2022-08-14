from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import Group
from api.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


admin.site.unregister(Group)


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "position",
    )
    list_filter = ("position",)
    ordering = ("username",)
    list_display = (
        "username",
        "id",
        "first_name",
        "last_name",
        "email",
        "position",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {"fields": ("username", "first_name", "last_name", "email", "password")},
        ),
        ("Position", {"fields": ("position",)}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                    "position",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )

    def has_module_permission(self, request):
        return True

    @method_decorator(login_required)
    def has_add_permission(self, request):
        if request.user.is_superuser is True:
            return True
        elif request.user.position == "MANAGEMENT":
            return True
        else:
            return False

    @method_decorator(login_required)
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser is True:
            return True
        elif request.user.position == "MANAGEMENT":
            return True
        else:
            return False

    @method_decorator(login_required)
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser is True:
            return True
        elif request.user.position == "MANAGEMENT":
            return True
        else:
            return False

    @method_decorator(login_required)
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser is True:
            return True
        elif request.user.position == "MANAGEMENT":
            return True
        else:
            return False

    # list_filter = ("position",)
    # ordering = ("position",)
    # search_fields = (
    #     "user_name",
    #     "last_name",
    #     "first_name",
    #     "email",
    #     "position",
    # )


admin.site.register(User, UserAdminConfig)
