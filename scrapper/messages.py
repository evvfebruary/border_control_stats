import time
import datetime
from loguru import logger
from typing import List, Tuple
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from scrapper.config import API_ID, API_HASH, FIRST_MESSAGE_WITH_LABEL_ID, SLEEP_VALUE, FAKE_PHONE, CHANNEL_LINK


def get_authorized_client():
    """
    Autohorize in Telegram API ( prompt needed for the first time )
    :return:
    """
    client = TelegramClient('border_control', API_ID, API_HASH)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(FAKE_PHONE)
        try:
            me = client.sign_in(FAKE_PHONE, input('Enter code: '))
        except Exception as err:
            logger.error(err)
    return client, client.is_connected()


def get_messages_from_channel(client, channel, min_id) -> List[dict]:
    new_messages = []
    offset_id = 0
    while True:
        logger.info("# Get new messages")
        history = client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=10_000,
            max_id=0,
            min_id=min_id,
            hash=0
        ))

        messages = history.messages
        logger.info(f"#Got messages: {len(messages)}")

        if messages:
            offset_id = messages[-1].to_dict().get("id", 0)
            for message in messages:
                new_messages.append(message.to_dict())
            logger.info(f"# Last offset id: {offset_id}")
        else:
            break

        time.sleep(SLEEP_VALUE)
    return new_messages


def get_messages_from_border_control(min_id: int = FIRST_MESSAGE_WITH_LABEL_ID) -> Tuple[List[dict], datetime.datetime]:
    scrap_date = datetime.datetime.now()
    client, is_connected = get_authorized_client()
    border_control_channel = client.get_entity(CHANNEL_LINK)
    logger.info(f"# Border control {min_id}, {type(min_id)}")
    messages = get_messages_from_channel(client, border_control_channel, min_id)
    return messages, scrap_date
