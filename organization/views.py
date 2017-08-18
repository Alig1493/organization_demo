from rest_framework.permissions import IsAuthenticated

from organization.models import IFrame, Organization
from rest_framework import generics
# Create your views here.
from organization.serializers import IFrameSerializer, IFrameListSerializer
from .permissions import OrganizationPermission


class IFrameListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, OrganizationPermission,)

    def get_serializer_class(self):
        if self.request.POST:
            return IFrameSerializer
        else:
            return IFrameListSerializer

    def get_queryset(self):
        return IFrame.objects.filter(organization__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(organization=Organization.objects.get(user=self.request.user,
                                                              created_by=self.request.user))


class IFrameDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, OrganizationPermission,)
    serializer_class = IFrameSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'iframe_id'

    def get_queryset(self):
        return IFrame.objects.filter(organization__user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(organization=Organization.objects.get(user=self.request.user,
                                                              updated_by=self.request.user))
