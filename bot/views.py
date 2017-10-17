import json
from rest_framework import generics, status
from django.http import HttpResponse

# Create your views here.
from rest_framework.permissions import AllowAny

from bot.permissions import FacebookAuthentication
from bot.serializers import (MessengerPayloadSerializer, DummySerializer)


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
        # fb_id = []
        #
        # print("Payload:")
        # print(f"{request.data}\n\n")
        # print("Decoded Body Message: ")
        #
        # for item, content in request.data.items():
        #     if isinstance(content, list):
        #         print(f"Printing {item} list:")
        #         for obj in content:
        #             if isinstance(obj, dict):
        #                 for a, b in obj.items():
        #                     if a == 'id':
        #                         fb_id.append(b)
        #                     if isinstance(b, list):
        #                         print(f"Printing {a} list:")
        #                         for c in b:
        #                             if isinstance(c, dict):
        #                                 for d, e in c.items():
        #                                     if isinstance(e, dict):
        #                                         print(f"Printing {d} items:")
        #                                         for f, g in e.items():
        #                                             if f == 'id':
        #                                                 fb_id.append(g)
        #                                             print(f"{f} has {g}")
        #                                     else:
        #                                         print(f"{d} has {e} \n\n")
        #                             else:
        #                                 print(f"{c}\n\n")
        #                     else:
        #                         print(f"{a} has {b}\n\n")
        #             else:
        #                 print(f"{obj}\n\n")
        #     else:
        #         print(f"{item} has {content}\n\n")
        # print(f"fb_char_id = {fb_id}")
        try:
            super().create(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return HttpResponse()


class DummyView(generics.CreateAPIView):
    serializer_class = DummySerializer
    permission_classes = [AllowAny]
