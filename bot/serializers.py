from django.db import transaction
from rest_framework import serializers

from bot import fields
from bot.utils import save_page_message_entry
from bot.models import (FacebookIdModel, MessageDetailModel, MessagingModel,
                        MessengerPayloadModel, EntryModel, PayloadModel, AttachmentModel,
                        SendMessagingModel)


class FacebookIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = FacebookIdModel
        fields = ('id',)

    id = serializers.IntegerField(source='fb_id')


class PayloadSerializer(serializers.ModelSerializer):

    class Meta:
        model = PayloadModel
        fields = '__all__'


class AttachmentSerializer(serializers.ModelSerializer):

    url = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = AttachmentModel
        exclude = ('message', )

    type = serializers.CharField(max_length=1000)
    payload = PayloadSerializer(required=False, allow_null=True)


class MessageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageDetailModel
        fields = '__all__'

    attachments = AttachmentSerializer(many=True, required=False)
    text = serializers.CharField(required=False)
    type = serializers.CharField(required=False)


class MessagingSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessagingModel
        fields = ('timestamp', 'message', 'sender', 'recipient',)

    sender = FacebookIdSerializer()
    recipient = FacebookIdSerializer()
    timestamp = fields.UnixDateTimeField(input_formats=['unix_timestamp'])
    message = MessageDetailSerializer()


class EntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = EntryModel
        fields = ('time', 'id', 'messaging')

    time = fields.UnixDateTimeField(input_formats=['unix_timestamp'])
    messaging = MessagingSerializer(many=True)
    id = serializers.IntegerField(source='fb_id')


class MessengerPayloadSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessengerPayloadModel
        fields = '__all__'

    object = serializers.CharField(allow_blank=True)
    entry = EntrySerializer(many=True, write_only=True)

    def create(self, validated_data):
        with transaction.atomic():
            entry_data = validated_data.pop('entry', '')
            obj = super().create(validated_data)

            if obj.object == "page":
                save_page_message_entry(entry_data, obj)

            return obj


class SendMessagingSerializer(serializers.ModelSerializer):

    message = MessageDetailSerializer()
    recipient = FacebookIdSerializer()

    class Meta:
        model = SendMessagingModel
        fields = ('messaging_type', 'recipient', 'message')
