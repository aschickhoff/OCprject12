from api.models import Client
from api.serializers import ClientSerializer
from EpicEvents.permissions import IsManagement, IsSales
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsManagement | IsSales]
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_queryset(self, *args, **kwargs):
        if self.request.user.position != "SUPPORT":
            return Client.objects.all()
        #  otherwise show customers from events that I support


# email needs to be verified when creating user
