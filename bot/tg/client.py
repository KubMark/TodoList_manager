import logging
import requests
from pydantic import ValidationError
from bot.tg.dc import GetUpdatesResponse, SendMessageResponse
<<<<<<< HEAD
from todolist import settings
=======
>>>>>>> origin/dev38_telegram_bot

logger = logging.getLogger(__name__)


class TgClient:
<<<<<<< HEAD
    def __init__(self, token: str = settings.TELEGRAM_TOKEN):
=======
    def __init__(self, token: str):
>>>>>>> origin/dev38_telegram_bot
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
<<<<<<< HEAD
            logger.error(f'Пришли неверные данные: {data}')

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """Requests TG bot using sendMessage"""
        response = requests.get(self.get_url('SendMessage'), params={'chat_id': chat_id, 'text': text})
=======
            logger.error(f'Пришли не верные данные: {data}')


    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """Requests TG bot using sendMessage"""
        response = requests.get(self.get_url('SendMessage'), params={'chat_id': chat_id, 'text': text}).json()
>>>>>>> origin/dev38_telegram_bot
        data = response.json()
        try:
            return SendMessageResponse(**data)
        except ValidationError:
<<<<<<< HEAD
            logger.error(f'Пришли неверные данные: {data}')
=======
            logger.error(f'Пришли не верные данные: {data}')
>>>>>>> origin/dev38_telegram_bot
