from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.owner == request.user


class IsOwnerOrStaff(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user or request.user.is_staff:
            return True
        else:
            print('False')
            return False


class IsAutentificated(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return True
        else:
            return obj.owner == request.user