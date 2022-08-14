from django.db import models
from .clients import Client
from .users import POS_CHOICES, User
from .eventstatus import EventStatus


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        limit_choices_to={"position": POS_CHOICES[1][0]},
        blank=True,
        null=True,
    )
    event_status = models.ForeignKey(
        EventStatus, default="1", on_delete=models.SET_NULL, blank=True, null=True
    )
    attendees = models.IntegerField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Event#{self.event_id}: {self.event_date} - {self.client.first_name} {self.client.last_name}"
