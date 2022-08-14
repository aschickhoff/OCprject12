from api.models import Contract
from api.serializers import ContractSerializer
from django_filters.rest_framework import DjangoFilterBackend
from EpicEvents.permissions import IsSales
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class ContractViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSales]
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "client__first_name",
        "client__last_name",
        "client__email",
        "date_created",
        "date_updated",
        "amount",
    ]
    queryset = Contract.objects.all()

    def get_queryset(self, *args, **kwargs):
        if self.request.user.position == "MANAGEMENT":
            return Contract.objects.all()
        elif self.request.user.position == "SALES":
            return Contract.objects.filter(sales_contact=self.request.user)
        elif self.request.user.position == "SUPPORT":
            return Contract.objects.filter(event__support_contact=self.request.user)
