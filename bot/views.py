from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from bot.permissions import HasToken


class Message(APIView):
    permission_classes = [HasToken]

    def get(self):
        """
        Returns a hub challenge back to messenger if 
        permission is allowed
        """
        return Response(self.request.GET['hub.challenge'])
