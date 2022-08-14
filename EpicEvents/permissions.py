from rest_framework import permissions


class IsManagement(permissions.BasePermission):
    message = "You need to be member of the management team!"

    def has_permission(self, request, view):
        if request.user.position == "MANAGEMENT":
            return True
        else:
            return request.method == "GET"

    def has_object_permission(self, request, view, obj):
        if request.user.position == "MANAGEMENT":
            return True
        else:
            return request.method == "GET"


class IsSales(permissions.BasePermission):
    message = "You need to be a member of the sales or management team!"

    def has_permission(self, request, view):
        if request.user.position == "SALES":
            return request.method in ["GET", "POST", "PATCH"]
        else:
            return request.method == "GET"

    def has_object_permission(self, request, view, obj):
        if request.user.position == "SALES":
            return request.method in ["GET", "PATCH"]
        else:
            return request.method == "GET"


class IsClientSalesContact(permissions.BasePermission):
    message = "You need to be the sales contact person of the client!"


class IsSupport(permissions.BasePermission):
    message = "You need to be a member of the support team!"


class IsClientSupportContact(permissions.BasePermission):
    message = "You need to be the support contact person of the client!"
