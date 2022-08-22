from django.contrib import admin
from api.models import Contract, Client
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    management_fieldset = (("Sales agent", {"fields": ("sales_contact",)}),)
    sales_fieldset = (("Sales agent", {"fields": ("sales_contact",)}),)
    fieldsets = (
        ("Contract", {"fields": ("client",)}),
        ("Date", {"fields": ("date_created", "date_updated")}),
        ("Payment", {"fields": ("amount", "payment_due", "status")}),
    )
    list_display = (
        "contract_id",
        "client",
        "sales_contact",
        "amount",
        "payment_due",
        "status",
        "date_created",
        "date_updated",
    )
    list_filter = ("sales_contact", "status")
    ordering = ("contract_id",)
    readonly_fields = ("date_created", "date_updated")
    search_fields = (
        "client__first_name",
        "client__last_name",
        "client__email",
        "date_updated",
        "amount",
    )
    list_display_links = (
        "contract_id",
        "client",
    )

    def get_fieldsets(self, request, obj=None):
        if request.user.position == "MANAGEMENT" and self.management_fieldset:
            return (self.fieldsets or tuple()) + self.management_fieldset
        elif request.user.position == "SALES" and self.sales_fieldset:
            return (self.fieldsets or tuple()) + self.sales_fieldset
        return super(ContractAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ContractAdmin, self).get_form(request, obj, **kwargs)
        if request.user.position == "SALES":
            form.base_fields["sales_contact"].initial = request.user
            form.base_fields["sales_contact"].disabled = True
        return form

    def render_change_form(self, request, context, *args, **kwargs):
        if request.user.position == "MANAGEMENT":
            return super(ContractAdmin, self).render_change_form(
                request, context, *args, **kwargs
            )
        elif request.user.position == "SALES":
            context["adminform"].form.fields["client"].queryset = Client.objects.filter(
                sales_contact=request.user
            )
            return super(ContractAdmin, self).render_change_form(
                request, context, *args, **kwargs
            )
        return super(ContractAdmin, self).render_change_form(
            request, context, *args, **kwargs
        )

    def get_queryset(self, request):
        instance = super(ContractAdmin, self).get_queryset(request)
        if request.user.position == "MANAGEMENT":
            return instance.all()
        elif request.user.position == "SALES":
            return instance.filter(sales_contact=request.user)
        elif request.user.position == "SUPPORT":
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
