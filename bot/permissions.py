from rest_framework import permissions
from cramstack_demo.settings import VERIFICATION_TOKEN


class HasToken(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method == "POST":
            return True

        if request.method == "GET":
            print("get request")
            print(request.GET)
            if request.GET.get('hub.verify_token', '') == VERIFICATION_TOKEN:
                print("Verification token matches")
                return True
            return False
