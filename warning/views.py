from django.shortcuts import render
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView,
                                     RetrieveDestroyAPIView, CreateAPIView)
from rest_framework.permissions import AllowAny

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
