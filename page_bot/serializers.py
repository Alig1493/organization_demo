from django.db import transaction
from rest_framework import serializers

from bot import fields
from page_bot.models import PagePayloadModel, PageEntryModel, PageChangesModel, PageValueModel, PageFromModel


class PageFromSerializer(serializers.ModelSerializer):

    class Meta:
        model = PageFromModel
        fields = '__all__'


class PageValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = PageValueModel
        fields = '__all__'


class PageChangesSerializer(serializers.ModelSerializer):
    value = PageValueSerializer(required=True)

    class Meta:
        model = PageChangesModel
        fields = '__all__'


class PageEntrySerializer(serializers.ModelSerializer):
    changes = PageChangesSerializer(many=True)

    class Meta:
        model = PageEntryModel
        fields = '__all__'


class PagePayloadSerializer(serializers.ModelSerializer):
    entry = PageEntrySerializer(many=True)

    class Meta:
        model = PagePayloadModel
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        for items in validated_data['entry']:
            print(dict(items))
            print(dict(items).pop('changes', ''))
            for sub_items in dict(items).pop('changes', ''):
                print(dict(sub_items))
                print(dict(dict(sub_items).pop('value','')))
        print(super().is_valid())
        return validated_data
