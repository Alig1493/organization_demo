import json

from warning.models import User


def get_started(sender_detail, user_details):
    message_content = f"Hello {user_details['first_name']}. How can I assist you today?"
    return json.dumps({"messaging_type": "RESPONSE",
                       "recipient": {"id": sender_detail.fb_id,
                                     "name": user_details['first_name']},
                       "message": {
                           "text": message_content,
                           "quick_replies": [
                               {
                                   "content_type": "text",
                                   "title": "Get Started!",
                                   "payload": "<POSTBACK_PAYLOAD>"
                               }
                           ]
                       }
                       })


def find_teacher(sender_detail, user_details):
    print("Inside Find Teacher")
    message_content = f"Hello {user_details['first_name']}. These are the teachers available "
    list_of_people = User.objects.all().values_list("name", flat=True)
    people = []
    for person in list_of_people:
        people.append({
            "content_type": "text",
            "title": f"{person}",
            "payload": "<POSTBACK_PAYLOAD>"
        })
    return json.dumps({"messaging_type": "RESPONSE",
                       "recipient": {"id": sender_detail.fb_id,
                                     "name": user_details['first_name']},
                       "message": {
                           "text": message_content,
                           "quick_replies": people or [{
                               "content_type": "text",
                               "title": f"No one available!",
                               "payload": "<POSTBACK_PAYLOAD>"
                           }]
                       }
                       })


def contact_teacher(sender_detail, user_details, teacher_details):
    message_content = f"Hello {user_details['first_name']}. How can I assist you today?" \
                      f"\nYou can contact your teacher through here:"
    return json.dumps({"messaging_type": "RESPONSE",
                       "recipient": {"id": sender_detail.fb_id,
                                     "name": user_details['first_name']},
                       "message": {
                           "attachment": {
                               "type": "template",
                               "payload": {
                                   "template_type": "generic",
                                   "elements": [
                                       {
                                           "title": message_content,
                                           "subtitle": (f"Name: {teacher_details.name}\n"
                                                        f"Phone: {teacher_details.phone}"),
                                       }
                                   ]
                               }
                           }
                       }
                       })
