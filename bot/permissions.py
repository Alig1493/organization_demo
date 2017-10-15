from rest_framework import permissions

from bot.config import verify_signature
from cramstack_demo.settings import VERIFICATION_TOKEN


class FacebookAuthentication(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method == "POST":
            if verify_signature(request):
                return True
            return False

        if request.method == "GET":
            if request.GET.get('hub.verify_token', '') == VERIFICATION_TOKEN:
                return True
            return False
