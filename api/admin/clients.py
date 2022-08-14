from django.contrib import admin
from api.models import Client
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Client",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "company_name",
                    "email",
                    "phone",
                    "mobile",
                )
            },
        ),
        ("Sales agent", {"fields": ("sales_contact",)}),
        ("Client status", {"fields": ("client_status",)}),
        ("Date", {"fields": ("date_created", "date_updated")}),
    )
    list_display = (
        "company_name",
        "last_name",
        "first_name",
        "email",
        "phone",
        "mobile",
        "sales_contact",
        "client_status",
    )
    list_filter = ("sales_contact",)
    ordering = ("company_name",)
    readonly_fields = ("date_created", "date_updated")
    search_fields = (
        "last_name",
        "first_name",
        "email",
        "phone",
        "mobile",
        "company_name",
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(ClientAdmin, self).get_form(request, obj, **kwargs)
        if request.user.position == "SALES":
            form.base_fields["sales_contact"].initial = request.user
            form.base_fields["sales_contact"].disabled = True
        return form

    def get_queryset(self, request):
        instance = super(ClientAdmin, self).get_queryset(request)
        if request.user.position == "MANAGEMENT":
            return instance.all()
        if request.user.position == "SALES":
            return instance.filter(sales_contact=request.user)
        if request.user.position == "SUPPORT":
            return instance.filter(event__support_contact=request.user)

    def has_module_permission(self, request):
        return True

    @method_decorator(login_required)
    def has_add_permission(self, request):
        if request.user.is_superuser is True:
            return True
        elif request.user.position == "SALES":
            return True
        else:
            return False

    @method_decorator(login_required)
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser is True:
            return True
        elif request.user.position == "MANAGEMENT":
            return True
        elif request.user.position == "SALES":
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser is True:
            return True
        else:
            return False

    @method_decorator(login_required)
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser is True:
            return True
        elif request.user.position == "MANAGEMENT":
            return True
        elif request.user.position == "SALES":
            return True
        elif request.user.position == "SUPPORT":
            return True
        else:
            return False
