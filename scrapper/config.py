import os
from dotenv import load_dotenv

load_dotenv('scrapper/.env')

# Channel attributes
CHANNEL_ID = '1776583381'
FIRST_MESSAGE_WITH_LABEL_ID = 1640
CHANNEL_LINK = 'https://t.me/+yHACAsBxEXo4OGEy'

# Telegram API credentials and params
SLEEP_VALUE = 60 + 5
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
FAKE_PHONE = os.getenv('FAKE_PHONE')


