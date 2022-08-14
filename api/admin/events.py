from django.contrib import admin
from api.models import Event, Contract, Client
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Event",
            {
                "fields": (
                    "client",
                    "contract",
                    "attendees",
                )
            },
        ),
        ("Support agent", {"fields": ("support_contact",)}),
        ("Date", {"fields": ("event_date",)}),
        ("Notes", {"fields": ("notes",)}),
        ("Status", {"fields": ("event_status",)}),
    )
    list_display = (
        "event_id",
        "client",
        "support_contact",
        "event_date",
        "attendees",
        "event_status",
    )
    list_filter = ("support_contact", "event_status")
    ordering = ("event_date",)
    search_fields = (
        "client__first_name",
        "client__last_name",
        "client__email",
        "event_date",
    )
    list_display_links = (
        "event_id",
        "client",
    )

    def get_readonly_fields(self, request, obj=None):
        if request.user.position == "SALES":
            return "support_contact"
        if request.user.position == "SUPPORT":
            return ("client", "support_contact")
            # if str(obj.event_status) != "Closed":
            #     return ("client", "support_contact")
            # else:
            #     return (
            #         "client",
            #         "attendees",
            #         "event_date",
            #         "support_contact",
            #         "notes",
            #         "event_status",
            #     )
        return super(EventAdmin, self).get_readonly_fields(request, obj=obj)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(EventAdmin, self).get_form(request, obj, **kwargs)
        if request.user.position == "SALES":
            form.base_fields["client"].queryset = Client.objects.filter(
                sales_contact=request.user
            )
            form.base_fields["contract"].queryset = Contract.objects.filter(
                clients__sales_contact=request.user
            )
        return form

    def get_queryset(self, request):
        instance = super(EventAdmin, self).get_queryset(request)
        if request.user.position == "MANAGEMENT":
            return instance.all()
        if request.user.position == "SALES":
            return instance.filter(client__sales_contact=request.user)
        # if request.user.position == "SUPPORT":
        #     return instance.filter(support_contact=request.user) & instance.exclude(
        #         event_status=7
        #     )  # 7 is closed
        if request.user.position == "SUPPORT":
            return instance.filter(support_contact=request.user)

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
            return False
        elif request.user.position == "SUPPORT":
            if obj is None:
                return True
            else:
                if str(obj.event_status) == "Closed":
                    return False
                else:
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
