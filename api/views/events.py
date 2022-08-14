from api.models import Event
from api.serializers import EventSerializer
from EpicEvents.permissions import IsSales
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSales]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_queryset(self, *args, **kwargs):
        if self.request.user.position == "MANAGEMENT":
            return Event.objects.all()
        elif self.request.user.position == "SALES":
            return Event.objects.filter(contract__sales_contact=self.request.user)
        elif self.request.user.position == "SUPPORT":
            return Event.objects.filter(support_contact=self.request.user)
