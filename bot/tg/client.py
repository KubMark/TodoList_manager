import logging
from enum import Enum
from typing import Any
from django.conf import settings
import requests
from pydantic import ValidationError

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse

logger = logging.getLogger(__name__)

class Command(str, Enum):
    GET_UPDATES = 'getUpdates'
    SEND_MESSAGE = 'sendMessage'


class TgClient:

    def __init__(self, token: str = settings.TELEGRAM_TOKEN):
        self.token = token

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        data = self._get(Command.GET_UPDATES, offset=offset, timeout=timeout)
        try:
            return GetUpdatesResponse(**data)
        except ValidationError:
            logger.warning(data)
            return GetUpdatesResponse(ok=False, result=[])

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        data = self._get(Command.SEND_MESSAGE, chat_id=chat_id, text=text)
        return SendMessageResponse(**data)

    def get_url(self, command: Command):
        return f'https://api.telegram.org/bot{self.token}/{command.value}'

    def _get(self, command: Command, **params: Any) -> dict:
        url = self.get_url(command)
        response = requests.get(url, params=params)
        if not response.ok:
            raise ValueError
        return response.json()
