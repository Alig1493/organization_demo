import json
import os

import re

import urllib.request

import requests
from django.core.files import File

from bot.config import UserType
from bot.models import FacebookIdModel, MessageDetailModel, MessagingModel, EntryModel, PayloadModel, AttachmentModel
# from bot.serializers import SendMessagingSerializer, FacebookIdSerializer, MessageDetailSerializer
from cramstack_demo.settings import PAGE_ACCESS_TOKEN
from page_bot.models import PageSubscribersModel

message_types = ["text", "attachments"]


def save_page_message_entry(entry_data, obj):

    for entry in entry_data:
        entry_dict = dict(entry)
        facebook_id = entry_dict.pop('fb_id', '')
        time = entry_dict.pop('time', '')

        entry_detail = EntryModel.objects.create(fb_id=facebook_id, time=time, messenger_payload=obj)
        save_messaging(entry_dict.pop('messaging', ''), entry_detail)


def save_messaging(messaging, entry_detail):

    for content in messaging:
        messaging_info = dict(content)
        message_info = dict(messaging_info.pop('message', ''))
        message_detail = MessageDetailModel.objects.create(mid=message_info['mid'],
                                                           seq=message_info['seq'])

        save_message_info(message_info, message_detail)
        save_user_info(message_detail, messaging_info.pop('timestamp', ''), dict(messaging_info.pop('sender', '')),
                       dict(messaging_info.pop('recipient', '')), entry_detail)


def save_message_info(message_info, message_detail):

    if "text" in message_info:
        print("inside text")
        text_message_object_save(message_info, message_detail)
    else:
        print("not inside text")
        attachment_message_object_save(message_info, message_detail)


def save_user_info(message_detail, timestamp_info, sender_info, recipient_info, entry_detail):

    sender_detail = FacebookIdModel.objects.create(fb_id=sender_info['fb_id'],
                                                   user_type=UserType.SENDER)
    recipient_detail = FacebookIdModel.objects.create(fb_id=recipient_info['fb_id'],
                                                      user_type=UserType.RECIPIENT)

    MessagingModel.objects.create(message=message_detail, timestamp=timestamp_info,
                                  sender=sender_detail, recipient=recipient_detail,
                                  entry=entry_detail)

    send_facebook_message(sender_detail, message_detail)


def retrieve_user_facebook_information(sender_detail):

    user_details_url = f"https://graph.facebook.com/v2.11/{sender_detail.fb_id}"
    user_details_params = {'access_token': PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()
    print("Current user details: " + json.dumps(user_details))
    print(f"Hello {user_details['first_name']}")
    return user_details


def text_message_object_save(message_info, message_detail):

    text_attachment = AttachmentModel.objects.create(type='text', text=message_info['text'], message=message_detail)
    print("--------------------------")
    if "attachments" in message_info:
        save_text_attachment(text_attachment, message_info['attachments'])


def save_text_attachment(text_attachment, attachment_payload):

    print(attachment_payload)
    for items in attachment_payload:
        print("---------------------------")
        print(dict(items))
        print("---------------------------")
        file_content = re.split('[/&+=?]+', f"{items['url']}")
        print(file_content)
        payload_object = PayloadModel.objects.create(url=items['url'])
        text_attachment.title = items['title']
        text_attachment.type = items['type']
        text_attachment.payload = payload_object
        text_attachment.save()


def attachment_message_object_save(message_info, message_detail):

    for content in message_info['attachments']:
        content_type = content.pop('type', '')
        payload = content.pop('payload', '')
        title = ""

        if payload is not None:
            payload = dict(payload)
            print(payload)
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

            AttachmentModel.objects.create(title=title, type=content_type,
                                           payload=payload_object, message=message_detail)


def send_facebook_message(sender_detail, message_detail):

    message_content = ""

    attachment_payload = AttachmentModel.objects.get(message=message_detail)

    if attachment_payload.text:
        message_content += AttachmentModel.objects.get(message=message_detail).text
    else:
        message_content += AttachmentModel.objects.get(message=message_detail).payload.url

    # Get user details:
    user_details = retrieve_user_facebook_information(sender_detail)

    # save subscriber
    if len(PageSubscribersModel.objects.filter(subscriber_id=sender_detail.fb_id)) == 0:
        PageSubscribersModel.objects.create(subscriber_name=user_details['first_name'],
                                            subscriber_id=sender_detail.fb_id)
        message_content += "\nYou have been registered!"

    # Post message to user:
    send_text_message_to_facebook_users(sender_detail, user_details, message_content)


def send_text_message_to_facebook_users(sender_detail, user_details, message_content):

    message_url = f"https://graph.facebook.com/v2.11/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    # messaging_reply_content = json.dumps({"messaging_type": "RESPONSE",
    #                                       "recipient": {"id": sender_detail.fb_id,
    #                                                     "name": user_details['first_name']},
    #                                       "message": {"text": f"Hello {user_details['first_name']}. "
    #                                                           f"How can I assist you today?"
    #                                                           f"\nYour message: {message_content}"}
    #                                       })
    # message_content = (f"Hello {user_details['first_name']}. How can I assist you today? "
    #                    f"\nYour message: {message_content}")
    # messaging_reply_content = SendMessagingSerializer(recipient=FacebookIdSerializer(id=sender_detail.fb_id),
    #                                                   message=MessageDetailSerializer(type="text",
    #                                                                                   text=message_content))
    # print(messaging_reply_content.is_valid())
    # status = requests.post(message_url, headers={"Content-Type": "application/json"},
    #                        data=messaging_reply_content)
    # print(status.json())
