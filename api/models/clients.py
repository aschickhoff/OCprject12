from django.db import models
from .users import POS_CHOICES, User

CLIENT_STATUS = (("POTENTIAL", "Potential"), ("EXISTING", "Existing"))


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=25, blank=True, null=True)
    mobile = models.CharField(max_length=25, blank=True, null=True)
    company_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        limit_choices_to={"position": POS_CHOICES[0][0]},
        blank=True,
        null=True,
    )
    client_status = models.CharField(
        choices=CLIENT_STATUS, default="POTENTIAL", max_length=10
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.company_name})"
