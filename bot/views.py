import json
from rest_framework import generics, status
from django.http import HttpResponse

# Create your views here.
from rest_framework.permissions import AllowAny

from bot.permissions import FacebookAuthentication
from bot.serializers import MessengerPayloadSerializer, MessagingSerializer, EntrySerializer, DummySerializer


class Message(generics.ListCreateAPIView):
    permission_classes = [FacebookAuthentication]
    serializer_class = MessengerPayloadSerializer

    def get_queryset(self):
        pass

    def list(self, request, *args, **kwargs):

        print(self.request.GET)
        return HttpResponse(self.request.GET["hub.challenge"], content_type="text/plain",
                            status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        try:
            super().create(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return HttpResponse()


class DummyView(generics.CreateAPIView):
    serializer_class = DummySerializer
    permission_classes = [AllowAny]
