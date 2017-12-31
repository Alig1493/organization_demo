from rest_framework import generics, status
from django.http import HttpResponse

from bot.permissions import FacebookAuthentication
from bot.serializers import (MessengerPayloadSerializer)


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
            print("Inside Message")
            super().create(request, *args, **kwargs)
        except Exception as e:
            print(e)
        return HttpResponse()
