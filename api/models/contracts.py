from django.db import models
from .users import POS_CHOICES, User
from .clients import Client


class Contract(models.Model):
    contract_id = models.AutoField(primary_key=True)
    sales_contact = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        limit_choices_to={"position": POS_CHOICES[0][0]},
        blank=True,
        null=True,
    )
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False, verbose_name="Signed")
    amount = models.FloatField(null=True)
    payment_due = models.DateField(blank=True, null=True)

    def __str__(self):
        return (f"Contract# {self.contract_id}: {self.client.first_name} {self.client.last_name} "
                f"- {self.client.company_name}")
