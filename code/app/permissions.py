from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow staff and owners of an object to view and edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST' and request.user.is_authenticated:
            return True
        # Instance must have an attribute named `owner`.
        return (obj.owner == request.user) or request.user.is_staff


class ReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow staff and owners of an object to view and edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET' and request.user.is_authenticated:
            return True
        # Instance must have an attribute named `owner`.
        return request.user.is_staff


class OwnerReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to view it.
    Staff can read and edit.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if (request.method == 'GET' and (obj.owner == request.user)) or request.user.is_staff:
            return True
        return False
