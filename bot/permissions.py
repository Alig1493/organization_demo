from rest_framework import permissions


class HasToken(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        print(request.GET['hub.verify_token'])
        if request.GET['hub.verify_token'] == 'ali123':
            return True
        return False
