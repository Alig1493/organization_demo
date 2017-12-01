import datetime

from django.db import transaction
from rest_framework import serializers

from bot import fields
from page_bot.models import PagePayloadModel, PageEntryModel, PageChangesModel, PageValueModel, PageFromModel
from page_bot.utils import save_page_post_entry


class PageFromSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='sender_id')

    class Meta:
        model = PageFromModel
        fields = ('id', 'name',)


class PageValueSerializer(serializers.ModelSerializer):

    from_object = PageFromSerializer()
    created_time = fields.UnixDateTimeField(input_formats=['unix_timestamp'])

    class Meta:
        model = PageValueModel
        fields = ('verb', 'item', 'message',
                  'post_id', 'published', 'from_object',
                  'created_time',)

    def to_internal_value(self, data):
        data['from_object'] = data.pop('from', '')
        return super(PageValueSerializer, self).to_internal_value(data)


class PageChangesSerializer(serializers.ModelSerializer):
    value = PageValueSerializer()

    class Meta:
        model = PageChangesModel
        exclude = ('page_entry',)


class PageEntrySerializer(serializers.ModelSerializer):
    changes = PageChangesSerializer(many=True)
    id = serializers.IntegerField(source='recipient_id')
    time = fields.UnixDateTimeField(input_formats=['unix_timestamp'])

    class Meta:
        model = PageEntryModel
        fields = ("changes", "id", "time",)


class PagePayloadSerializer(serializers.ModelSerializer):
    entry = PageEntrySerializer(many=True)

    class Meta:
        model = PagePayloadModel
        fields = '__all__'

    def create(self, validated_data):
        try:
            with transaction.atomic():
                print(validated_data)
                entry = validated_data.pop('entry', '')
                obj = super().create(validated_data)
                save_page_post_entry(obj, entry)
                print(obj)
                return obj
        except Exception as e:
            print(e)
