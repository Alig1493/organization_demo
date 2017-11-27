import json
import os

import re

import urllib.request

import requests
from django.core.files import File
from django.core.files.base import ContentFile

from bot.config import UserType
from bot.models import FacebookIdModel, MessageDetailModel, MessagingModel, EntryModel, PayloadModel, AttachmentModel
from cramstack_demo.settings import PAGE_ACCESS_TOKEN

message_types = ["text", "attachments"]


def save_page_message_entry(entry_data, obj):

    for entry in entry_data:
        entry_dict = dict(entry)
        facebook_id = entry_dict.pop('fb_id', '')
        time = entry_dict.pop('time', '')

        entry_detail = EntryModel.objects.create(fb_id=facebook_id, time=time, messenger_payload=obj)

        messaging = entry_dict.pop('messaging', '')
        for content in messaging:
            messaging_info = dict(content)
            timestamp_info = messaging_info.pop('timestamp', '')
            message_info = dict(messaging_info.pop('message', ''))
            sender_info = dict(messaging_info.pop('sender', ''))
            recipient_info = dict(messaging_info.pop('recipient', ''))
            message_detail = MessageDetailModel.objects.create(mid=message_info['mid'],
                                                               seq=message_info['seq'])

            if "text" in message_info:
                print("inside text")
                text_message_object_save(message_info, message_detail)
            if "attachments" in message_info:
                print("not inside text")
                attachment_message_object_save(message_info, message_detail)

            message_content = AttachmentModel.objects.get(message=message_detail).refresh_from_db()

            sender_detail = FacebookIdModel.objects.create(fb_id=sender_info['fb_id'],
                                                           user_type=UserType.SENDER)
            recipient_detail = FacebookIdModel.objects.create(fb_id=recipient_info['fb_id'],
                                                              user_type=UserType.RECIPIENT)

            MessagingModel.objects.create(message=message_detail, timestamp=timestamp_info,
                                          sender=sender_detail, recipient=recipient_detail,
                                          entry=entry_detail)
            user_details_url = f"https://graph.facebook.com/v2.11/{sender_detail.fb_id}"
            user_details_params = {'access_token': PAGE_ACCESS_TOKEN}
            user_details = requests.get(user_details_url, user_details_params).json()
            print("Current user details: " +json.dumps(user_details))
            print(f"Hello {user_details['first_name']}")


            message_url = f"https://graph.facebook.com/v2.11/me/messages?access_token={PAGE_ACCESS_TOKEN}"
            messaging_reply_content = json.dumps({"messaging_type": "RESPONSE",
                                                  "recipient": {"id": sender_detail.fb_id,
                                                                "name": user_details['first_name']},
                                                  "message": {"text": f"Hello {user_details['first_name']}. "
                                                                      f"How can I assist you today?"
                                                              f"\nYour message: {message_content}"}
                                                  })
            status = requests.post(message_url, headers={"Content-Type": "application/json"},
                                   data=messaging_reply_content)
            print(status.json())


def text_message_object_save(message_info, message_detail):
    AttachmentModel.objects.create(type='text', text=message_info['text'], message=message_detail)


def attachment_message_object_save(message_info, message_detail):

    for content in message_info['attachments']:
        payload = dict(content.pop('payload', ''))
        content_type = content.pop('type', '')

        file_content = re.split('[/&+=?]+', f"{payload['url']}")

        urllib.request.urlretrieve(payload['url'], file_content[4])
        # read bytes for python3 and plain read for python2
        data = File(open(file_content[4], 'rb'))
        payload_object = PayloadModel.objects.create(url=payload['url'])
        # the three parameters are file_name, file_type object and save args
        payload_object.file.save(file_content[4], data, save=True)
        os.remove(file_content[4])

        if 'sticker_id' in payload:
            payload_object.sticker_id = payload['sticker_id']
            payload_object.save()

        AttachmentModel.objects.create(type=content_type, payload=payload_object, message=message_detail)
