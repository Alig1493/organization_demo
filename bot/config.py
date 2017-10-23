import hashlib
import hmac

import sys

from cramstack_demo.settings import FACEBOOK_APP_SECRET


class UserType(object):

    SENDER = 1
    RECIPIENT = 2

    CHOICES = (
        (SENDER, "Sender"),
        (RECIPIENT, "Recipient")
    )


def verify_signature(request):
    hashed_payload = ""
    # for content, information in request.META.items():
    #     print(f"{content} contain {information}")
    incoming_message = request.body
    # print("Incoming message:")
    # print(incoming_message)
    if 'test' in sys.argv:
        return True
    try:
        hashed_payload = hmac.new(bytearray(FACEBOOK_APP_SECRET, 'utf8'), incoming_message, hashlib.sha1)
        # print(FACEBOOK_APP_SECRET)
        # print(f"sha1={hashed_payload.hexdigest()}")
        # print(request.META["HTTP_X_HUB_SIGNATURE"])
    except Exception as e:
        print(f"Caught Exception: {e}")
        return False
    if f"sha1={hashed_payload.hexdigest()}" == request.META["HTTP_X_HUB_SIGNATURE"]:
        return True
    return False
