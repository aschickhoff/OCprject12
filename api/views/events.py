from api.models import Event
from api.serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_queryset(self, *args, **kwargs):
        print(f" Args: {self.args}")
        print(f" Kwargs: {self.kwargs}")
        if self.request.user.position == "SUPPORT":
            return Event.objects.all()  # ToDo: only return events that I support
