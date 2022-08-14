from api.models import Contract, Client
from api.serializers import ContractSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class ContractViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()

    # def perform_create(self, request, *args, **kwargs):
    #     client = Client.objects.get(pk=self.kwargs["client_pk"])
    #     if self.request.user.position == "SALES":
    #         contract = request.save(client=client)

    def get_queryset(self, *args, **kwargs):
        print(f" Args: {self.args}")
        print(f" Kwargs: {self.kwargs}")
        if self.request.user.position != "SUPPORT":
            return (
                Contract.objects.all()
            )  # ToDo: only return contracts from that client
        #  otherwise show contracts from events that I support


# when creating a contract the sales_contact for the client needs to be updated automatically
# when creating a contract the client needs to be assigned automatically
