from api.models import Event
from api.serializers import EventSerializer
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateTimeFilter
from EpicEvents.permissions import IsSales
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class EventFilter(FilterSet):
    min_date = DateTimeFilter(field_name="event_date", lookup_expr="gte")
    max_date = DateTimeFilter(field_name="event_date", lookup_expr="lte")

    class Meta:
        model = Event
        fields = [
            "client__first_name",
            "client__last_name",
            "client__email",
            "event_date",
        ]


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSales]
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter
    queryset = Event.objects.all()

    def get_queryset(self, *args, **kwargs):
        if self.request.user.position == "MANAGEMENT":
            return Event.objects.all()
        elif self.request.user.position == "SALES":
            return Event.objects.filter(contract__sales_contact=self.request.user)
        elif self.request.user.position == "SUPPORT":
            return Event.objects.filter(support_contact=self.request.user)
