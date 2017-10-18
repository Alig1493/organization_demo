import hashlib
import hmac

from cramstack_demo.settings import FACEBOOK_APP_SECRET

from bot.models import (FacebookIdModel, MessageDetailModel, MessagingModel,
                        EntryModel)


def verify_signature(request):
    hashed_payload = ""
    # for content, information in request.META.items():
    #     print(f"{content} contain {information}")
    incoming_message = request.body
    try:
        hashed_payload = hmac.new(bytearray(FACEBOOK_APP_SECRET, 'utf8'), incoming_message, hashlib.sha1)
    except Exception as e:
        print(f"Caught Exception: {e}")
        return False
    if f"sha1={hashed_payload.hexdigest()}" == request.META["HTTP_X_HUB_SIGNATURE"]:
        return True
    return False


def save_page_message_entry(entry_data, obj):

    for entry in entry_data:
        entry_dict = dict(entry)
        facebook_id = entry_dict.pop('fb_id', '')
        time = entry_dict.pop('time', '')
        messaging = entry_dict.pop('messaging', '')
        messaging_info = dict(messaging.pop())
        timestamp_info = messaging_info.pop('timestamp', '')
        message_info = dict(messaging_info.pop('message', ''))
        sender_info = dict(messaging_info.pop('sender', ''))
        recipient_info = dict(messaging_info.pop('recipient', ''))

        entry_detail = EntryModel.objects.create(fb_id=facebook_id, time=time, messenger_payload=obj)

        message_detail = MessageDetailModel.objects.create(mid=message_info['mid'],
                                                           seq=message_info['seq'],
                                                           text=message_info['text'])
        sender_detail = FacebookIdModel.objects.create(fb_id=sender_info['fb_id'])
        recipient_detail = FacebookIdModel.objects.create(fb_id=recipient_info['fb_id'])

        MessagingModel.objects.create(message=message_detail, timestamp=timestamp_info,
                                      sender=sender_detail, recipient=recipient_detail,
                                      entry=entry_detail)
