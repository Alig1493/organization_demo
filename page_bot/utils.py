import json
import os

import re

import urllib.request

import requests
from django.core.files import File

from cramstack_demo.settings import PAGE_ACCESS_TOKEN
from page_bot.models import PageEntryModel, PageChangesModel, PageValueModel, PageFromModel


def save_page_post_entry(payload_object, entry):
    print("Inside save page post entry def")
    for item in entry:
        entry_item = dict(item)
        entry_object = PageEntryModel.objects.create(payload_model=payload_object,
                                                     recipient_id=entry_item.get('recipient_id', ''),
                                                     time=entry_item.get('time', ''))
        for sub_item in entry_item['changes']:
            changes_info = dict(sub_item)
            changes_object = PageChangesModel.objects.create(page_entry=entry_object,
                                                             field=changes_info.get('field', ''))
            # print(changes_object)
            value_info = changes_info.get('value', '')
            # print(value_info)
            from_info = value_info.pop('from_object', '')
            # print(from_info)
            print(value_info.get('verb', ''))
            print(value_info.get('item', ''))
            print(value_info.get('post_id', ''))
            print(value_info.get('published', ''))
            print(value_info.get('created_time', ''))
            print(value_info.get('message', ''))
            value_object = PageValueModel.objects.create(verb=value_info.get('verb', ''),
                                                         item=value_info.get('item', ''),
                                                         message=value_info.get('message', ''),
                                                         post_id=str(value_info.get('post_id', '')),
                                                         published=value_info.get('published', ''),
                                                         created_time=value_info.get('created_time', ''),
                                                         page_changes=changes_object)
            PageFromModel.objects.create(value=value_object, name=from_info.get('name', ''),
                                         sender_id=from_info.get('sender_id', ''))
