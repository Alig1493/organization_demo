from rest_framework import serializers
from  rest_framework.serializers import ValidationError

from warning.config import phone_validator
from warning.models import User, WarningSmsModel, LostModel

from page_bot.utils import get_object_or_none


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class WarningSerializer(serializers.ModelSerializer):

    class Meta:
        model = WarningSmsModel
        fields = '__all__'


class LostSerializer(serializers.ModelSerializer):

    class Meta:
        model = LostModel
        fields = ('phone', 'user', 'family', 'description',)

    def validate(self, attrs):
        super().validate(attrs)
        phone = attrs.get('phone', '')
        user = attrs.get('user', '')

        if (phone or user) is not None:
            if phone is not None:
                user = get_object_or_none(User, phone__iexact=phone)

                if user:
                    attrs['user'] = user
        else:
            raise ValidationError("Either phone or user must be present!")

        return attrs