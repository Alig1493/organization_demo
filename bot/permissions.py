from rest_framework import permissions


class HasToken(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if request.data['hub.verify_token'] == 'ali123':
            return True
        return False
