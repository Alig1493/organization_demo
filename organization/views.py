from rest_framework.permissions import IsAuthenticated

from organization.models import IFrame, Organization
from rest_framework import generics
# Create your views here.
from organization.serializers import IFrameSerializer


class IFrameListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = IFrameSerializer

    def get_queryset(self):
        print(IFrame.objects.filter(organization__user=self.request.user))
        return IFrame.objects.filter(organization__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(organization=Organization.objects.get(user=self.request.user))
