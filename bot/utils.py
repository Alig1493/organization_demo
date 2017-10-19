from bot.config import UserType
from bot.models import FacebookIdModel, MessageDetailModel, MessagingModel, EntryModel


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
                                                               seq=message_info['seq'],
                                                               text=message_info['text'])
            sender_detail = FacebookIdModel.objects.create(fb_id=sender_info['fb_id'],
                                                           user_type=UserType.SENDER)
            recipient_detail = FacebookIdModel.objects.create(fb_id=recipient_info['fb_id'],
                                                              user_type=UserType.RECIPIENT)

            MessagingModel.objects.create(message=message_detail, timestamp=timestamp_info,
                                          sender=sender_detail, recipient=recipient_detail,
                                          entry=entry_detail)
