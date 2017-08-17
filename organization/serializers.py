from rest_framework import serializers

from organization.models import IFrame


class IFrameSerializer(serializers.ModelSerializer):

    class Meta:
        model = IFrame
        fields = "__all__"
        read_only_fields = ["organization", ]
