from rest_framework import permissions


class IsAuthenticatedandIsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        return obj.user == request.user
