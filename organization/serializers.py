from rest_framework import serializers

from organization.models import IFrame


class IFrameSerializer(serializers.ModelSerializer):

    class Meta:
        model = IFrame
        fields = "__all__"
        read_only_fields = ["organization", ]


class IFrameListSerializer(serializers.ModelSerializer):
    organization_name = serializers.SerializerMethodField()

    class Meta:
        model = IFrame
        fields = ['title', 'url', 'organization_name']

    def get_organization_name(self, obj):
        return obj.organization.title
