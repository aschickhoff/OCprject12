from api.models import Contract
from api.serializers import ContractSerializer
from EpicEvents.permissions import IsSales
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class ContractViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSales]
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()

    # def perform_create(self, request, *args, **kwargs):
    #     client = Client.objects.get(pk=self.kwargs["client_pk"])
    #     if self.request.user.position == "SALES":
    #         contract = request.save(client=client)

    def get_queryset(self, *args, **kwargs):
        if self.request.user.position == "MANAGEMENT":
            return Contract.objects.all()
        elif self.request.user.position == "SALES":
            return Contract.objects.filter(sales_contact=self.request.user)
        elif self.request.user.position == "SUPPORT":
            return Contract.objects.filter(event__support_contact=self.request.user)
