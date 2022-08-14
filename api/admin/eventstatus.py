from django.contrib import admin
from api.models import EventStatus


@admin.register(EventStatus)
class EventStatusAdmin(admin.ModelAdmin):
    list_display = (
        "event_status_id",
        "event_status",
    )
    ordering = ("event_status_id",)
