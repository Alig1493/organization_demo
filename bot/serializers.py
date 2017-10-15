from rest_framework import serializers


class FacebookIdSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    id = serializers.IntegerField()


class MessageDetailSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    mid = serializers.CharField()
    seq = serializers.IntegerField()
    text = serializers.CharField()


class MessagingSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    sender = FacebookIdSerializer()
    recipient = FacebookIdSerializer()
    timestamp = serializers.IntegerField()
    message = MessageDetailSerializer()


class EntrySerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    id = serializers.CharField()
    time = serializers.DateTimeField()
    messaging = MessagingSerializer(many=True)


class MessengerPayloadSerializer(serializers.Serializer):

    def create(self, validated_data):
        print("Payload data in serializer:")
        print(validated_data.get['object'])
        print(validated_data.get['entry'])
        pass

    def update(self, instance, validated_data):
        pass

    object = serializers.CharField(allow_blank=True)
    entry = EntrySerializer(many=True)
