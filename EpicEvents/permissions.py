from rest_framework import permissions


class IsManagement(permissions.BasePermission):
    message = "You are not authorized!"

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
    message = "You are not authorized!"

    def has_permission(self, request, view):
        if request.user.position == "MANAGEMENT":
            return request.method in ["GET", "PATCH"]
        elif request.user.position == "SALES":
            return request.method in ["GET", "POST", "PATCH"]
        else:
            return request.method == "GET"

    def has_object_permission(self, request, view, obj):
        if request.user.position == "MANAGEMENT":
            return request.method in ["GET", "PATCH"]
        elif request.user.position == "SALES":
            return request.method in ["GET", "PATCH"]
        else:
            return request.method == "GET"
