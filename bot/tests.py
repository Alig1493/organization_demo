from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

import hashlib
import hmac

from cramstack_demo.settings import FACEBOOK_APP_SECRET


class FacebookPayload(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_post_text_payload(self):
        data = {
            "object": "page",
            "entry": [
                {
                    "id": "1144617102337592",
                    "time": 1508754864987,
                    "messaging": [
                        {
                            "sender": {
                                "id": "1841928899153954"
                            },
                            "recipient": {
                                "id": "1144617102337592"
                            },
                            "timestamp": 1508754864664,
                            "message": {
                                "mid": "mid.$cAAQRBclTCvtlehGCGFfSMw5Yq830",
                                "seq": 737684,
                                "text": "adsads"
                            }
                        }
                    ]
                }
            ]
        }

        url = reverse('messenger_bot:facebook_messages')
        request = self.client.post(url, data)
        print(request)
