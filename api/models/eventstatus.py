from django.db import models


class EventStatus(models.Model):
    event_status_id = models.AutoField(primary_key=True)
    event_status = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.event_status}"
