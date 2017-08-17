from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from organization.models import Organization


class OrganizationPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if (request.method == 'GET' or
            request.method == 'POST' or
            request.method == 'PATCH' or
            request.method == 'PUT'or
                request.method == 'DELETE'):
            if Organization.objects.filter(user=request.user).exists():
                return True
            raise ValidationError("Not part of any organization yet!")
        return super(OrganizationPermission, self).has_permission(request, view)
