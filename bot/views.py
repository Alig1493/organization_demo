from rest_framework import generics, status
from rest_framework.response import Response
from django.http import HttpResponse

# Create your views here.
from bot.permissions import HasToken


class Message(generics.ListCreateAPIView):
    permission_classes = [HasToken]

    def get_queryset(self):
        pass

    def get_serializer(self, *args, **kwargs):
        pass

    def list(self, request, *args, **kwargs):
        print(self.request.GET["hub.challenge"])
        return HttpResponse(self.request.GET["hub.challenge"], content_type="text/plain",
                            status=status.HTTP_200_OK)
