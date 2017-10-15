import hashlib
import hmac

from cramstack_demo.settings import FACEBOOK_APP_SECRET


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
