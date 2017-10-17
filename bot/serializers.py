from django.db import transaction
from rest_framework import serializers

from bot import fields
from bot.models import (FacebookIdModel, MessageDetailModel, MessagingModel,
                        MessengerPayloadModel, EntryModel, DummyModel)


class FacebookIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = FacebookIdModel
        fields = ('id',)

    id = serializers.IntegerField(source='fb_id')


class MessageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageDetailModel
        fields = '__all__'


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

    def create(self, validated_data):
        with transaction.atomic():
            try:
                messaging_data = validated_data.pop('messaging', '')
                entry = super().create(validated_data)
                print(messaging_data)

                for data in messaging_data:
                    print(data)
                    data.save(entry=dict(entry))

                return entry
            except Exception as e:
                print(e)


class MessengerPayloadSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessengerPayloadModel
        fields = '__all__'

    object = serializers.CharField(allow_blank=True)
    entry = EntrySerializer(many=True)

    def create(self, validated_data):
        with transaction.atomic():
            try:
                entry_data = validated_data.pop('entry', '')
                messaging = entry_data.pop('messaging', '')

                for entry in entry_data:
                    e = EntryModel.objects.create(**dict(entry), object=obj)
                    print(e.id)

                return obj
            except Exception as e:
                print(e)


class DummySerializer(serializers.ModelSerializer):

    class Meta:
        model = DummyModel
        fields = '__all__'

    date = fields.UnixDateTimeField(input_formats=['unix_timestamp'])
