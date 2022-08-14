from api.models import Client
from api.serializers import ClientSerializer
from django_filters.rest_framework import DjangoFilterBackend
from EpicEvents.permissions import IsSales
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSales]
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["first_name", "last_name", "email"]
    queryset = Client.objects.all()

    def get_queryset(self, *args, **kwargs):
        if self.request.user.position == "MANAGEMENT":
            return Client.objects.all()
        elif self.request.user.position == "SALES":
            return Client.objects.filter(sales_contact=self.request.user)
        elif self.request.user.position == "SUPPORT":
            return Client.objects.filter(event__support_contact=self.request.user)
        # else:
        #     # return User.objects.all()
        #     return User.objects.filter(username=self.request.user.username)


# email needs to be verified when creating user
