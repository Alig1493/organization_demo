import json
import os

import re

import urllib.request

import requests
from django.core.files import File

from bot.config import UserType
from bot.models import FacebookIdModel, MessageDetailModel, MessagingModel, EntryModel, PayloadModel, AttachmentModel
from cramstack_demo.settings import PAGE_ACCESS_TOKEN
