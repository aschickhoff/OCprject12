from django.contrib import admin
from api.models import Client
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    management_fieldset = (("Sales agent", {"fields": ("sales_contact",)}),)
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
    list_filter = ("client_status",)
    ordering = ("company_name",)
    readonly_fields = ("date_created", "date_updated")
    search_fields = (
        "last_name",
        "first_name",
        "email",
        "company_name",
    )

    def get_fieldsets(self, request, obj=None):
        if request.user.position == "MANAGEMENT" and self.management_fieldset:
            return (self.fieldsets or tuple()) + self.management_fieldset
        return super(ClientAdmin, self).get_fieldsets(request, obj)

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
