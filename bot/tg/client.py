import logging
import requests
from pydantic import ValidationError
from bot.tg.dc import GetUpdatesResponse, SendMessageResponse
from todolist import settings

logger = logging.getLogger(__name__)


class TgClient:
    def __init__(self, token: str = settings.TELEGRAM_TOKEN):
        self.token = token

    def get_url(self, method: str):
        """Returns url to TG bot in str format with requested method"""
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        """Requests TG bot using getUpdates"""
        response = requests.get(self.get_url('getUpdates'), params={'timeout': timeout, 'offset': offset})
        data = response.json()
        try:
            return GetUpdatesResponse(**data)
        except ValidationError:

            logger.error(f'Пришли неверные данные: {data}')

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """Requests TG bot using sendMessage"""
        response = requests.get(self.get_url('SendMessage'), params={'chat_id': chat_id, 'text': text}).json()
        data = response.json()
        try:
            return SendMessageResponse(**data)
        except ValidationError:

            logger.error(f'Пришли неверные данные: {data}')

