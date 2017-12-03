import json

import requests

from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView,
                                     RetrieveDestroyAPIView, CreateAPIView)
from rest_framework.permissions import AllowAny

from cramstack_demo.settings import PAGE_ACCESS_TOKEN
from warning.models import User, LostModel
from warning.serializers import UserSerializer, LostSerializer


class RegistrationView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]

    def perform_create(self, serializer):
        print(self.request.data)
        print()
        super().perform_create(serializer)


class LostView(ListCreateAPIView):
    queryset = LostModel.objects.all()
    serializer_class = LostSerializer
    permission_classes = [AllowAny, ]

    def perform_create(self, serializer):
        instance = serializer.save()
        message = f"{instance.user.name}'s family is lost.\n{instance.description}" \
                  f"\nMembers include:\n"
        for x in instance.family.values_list("name", flat=True):
            message += x + "\n"
        if instance.user.phone:
            message += f"\nContact him here:{instance.user.phone}"
        fb_page_url = f"https://graph.facebook.com/v2.11/feed?access_token={PAGE_ACCESS_TOKEN}&message={message}"
        status = requests.post(fb_page_url, headers={"Content-Type": "application/json"})
        print(status.json())
