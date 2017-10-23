from bot.config import UserType
from bot.models import FacebookIdModel, MessageDetailModel, MessagingModel, EntryModel, PayloadModel, AttachmentModel

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

            if "text" in message_info:
                message_detail = text_message_object_save(message_info)
            else:
                message_detail = attachment_message_object_save(message_info)

            sender_detail = FacebookIdModel.objects.create(fb_id=sender_info['fb_id'],
                                                           user_type=UserType.SENDER)
            recipient_detail = FacebookIdModel.objects.create(fb_id=recipient_info['fb_id'],
                                                              user_type=UserType.RECIPIENT)

            MessagingModel.objects.create(message=message_detail, timestamp=timestamp_info,
                                          sender=sender_detail, recipient=recipient_detail,
                                          entry=entry_detail)


def text_message_object_save(message_info):

    message_detail = MessageDetailModel.objects.create(mid=message_info['mid'],
                                                       seq=message_info['seq'])

    AttachmentModel.objects.create(type='text', text=message_info['text'], message=message_detail)

    return message_detail


def attachment_message_object_save(message_info):

    message_detail = MessageDetailModel.objects.create(mid=message_info['mid'],
                                                       seq=message_info['seq'])

    for content in message_info['attachments']:
        payload = dict(content.pop('payload', ''))
        content_type = content.pop('type', '')

        payload_object = PayloadModel.objects.create(url=payload['url'])

        if 'sticker_id' in payload:
            payload_object.sticker_id = payload['sticker_id']
            payload_object.save()

        AttachmentModel.objects.create(type=content_type, payload=payload_object, message=message_detail)

    return message_detail


