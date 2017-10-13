import json
from rest_framework import generics, status
from django.http import HttpResponse

# Create your views here.
from bot.permissions import FacebookAuthentication
from bot.serializers import MessengerPayloadSerializer


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
        print("Payload:")
        print(f"{request.data}\n\n")
        print("Decoded Body Message: ")
        for item, content in request.data.items():
            if isinstance(content, list):
                for obj in content:
                    if isinstance(obj, dict):
                        for a, b in obj.items():
                            if isinstance(b, list):
                                for c in b:
                                    if isinstance(c, dict):
                                        for d, e in c.items():
                                            if isinstance(e, dict):
                                                for f, g in e.items():
                                                    print(f"{f} has {g}\n\n")
                                            else:
                                                print(f"{d} has {e} \n\n")
                                    else:
                                        print(f"{c}\n\n")
                            else:
                                print(f"{a} has {b}\n\n")
                    else:
                        print(f"{obj}\n\n")
            else:
                print(f"{item} has {content}\n\n")
        return super(Message, self).create(request, *args, **kwargs)
