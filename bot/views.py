import json
from rest_framework import generics, status
from django.http import HttpResponse

# Create your views here.
from bot.permissions import FacebookAuthentication


class Message(generics.ListCreateAPIView):
    permission_classes = [FacebookAuthentication]

    def get_queryset(self):
        pass

    def get_serializer(self, *args, **kwargs):
        pass

    def list(self, request, *args, **kwargs):
        print(self.request.GET)
        return HttpResponse(self.request.GET["hub.challenge"], content_type="text/plain",
                            status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        print("Decoded Body Message: ")
        # print(json.loads(self.request.body.decode('utf-8'))['entry'])
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                print(message['message'])
                for content, information in message['message'].items():
                    print(f"{content} has {information}")

        # print(self.request.body)
        # print("Detailed contents: ")
        return HttpResponse()
