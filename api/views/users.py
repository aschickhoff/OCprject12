from api.models import User
from api.serializers import UserSerializer
from EpicEvents.permissions import IsManagement
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsManagement]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self, *args, **kwargs):
        management = User.objects.filter(position="MANAGEMENT")
        if self.request.user in management.all():
            return User.objects.all()
        else:
            # return User.objects.all()
            return User.objects.filter(username=self.request.user.username)


# class UserViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated, IsManagement]
#     serializer_class = RegisterUserSerializer
#     queryset = User.objects.all()

#     def get_queryset(self, *args, **kwargs):
#         management = User.objects.filter(position="MANAGEMENT")
#         if self.request.user in management.all():
#             return User.objects.all()
#         else:
#             return User.objects.filter(username=self.request.user)
