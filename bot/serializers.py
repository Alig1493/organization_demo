from rest_framework import serializers


class FacebookIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class MessageDetailSerializer(serializers.Serializer):
    mid = serializers.CharField()
    seq = serializers.IntegerField()
    text = serializers.CharField()


class MessagingSerializer(serializers.Serializer):
    sender = FacebookIdSerializer()
    recipient = FacebookIdSerializer()
    timestamp = serializers.IntegerField()
    message = MessageDetailSerializer()


class EntrySerializer(serializers.Serializer):
    id = serializers.CharField()
    time = serializers.DateTimeField()
    messaging = MessagingSerializer(many=True)


class MessengerPayloadSerializer(serializers.Serializer):
    object = serializers.CharField(allow_blank=True)
    entry = EntrySerializer(many=True)
