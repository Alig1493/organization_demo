import datetime

from rest_framework import serializers
from rest_framework.settings import api_settings


class UnixDateTimeField(serializers.DateTimeField):

    def datetime_parser(self, value, input_format):
        if input_format == 'unix_timestamp':
            # Value needs to be of int type before being used in from timestamp
            return datetime.datetime.fromtimestamp(int(value)/1000)
        else:
            super().datetime_parser(value, input_format)
