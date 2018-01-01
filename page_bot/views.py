import json

import requests
from rest_framework import generics, status
from django.http import HttpResponse

from bot.models import MessagingModel, AttachmentModel
from bot.permissions import FacebookAuthentication
from bot.serializers import MessengerPayloadSerializer
from cramstack_demo.settings import PAGE_ACCESS_TOKEN
from page_bot.serializers import PagePayloadSerializer


class Post(generics.ListCreateAPIView):
    permission_classes = [FacebookAuthentication]

    def get_attachment_detail(self, data):
        return AttachmentModel.objects.get(
            message=MessagingModel.objects.get(entry__messenger_payload=data['id']).message)

    def get_serializer_class(self):
        if 'changes' in self.request.data['entry'][0].keys():
            return PagePayloadSerializer
        return MessengerPayloadSerializer

    def get_queryset(self):
        pass

    def list(self, request, *args, **kwargs):
        print(self.request.GET)
        return HttpResponse(self.request.GET["hub.challenge"], content_type="text/plain",
                            status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            # super().create(request, *args, **kwargs)
            # print(serializer.data)
            # print(dir(serializer))
            # print("FUCKING QUERY SHIT!!!!")
            # attachment = self.get_attachment_detail(data=serializer.data)
            # print(attachment.text)
            # print(attachment.text is None)
            # print(attachment.payload)
            # print(attachment.payload is None)

        except Exception as e:
            print(e)
        return HttpResponse()
