from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()

    def handle(self, *args, **options):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(tg_chat_id=msg.chat.id)
        if tg_user.user:
            self.handle_authorized(tg_user, msg)
        else:
            self.handle_unauthorized(tg_user, msg)

    def handle_authorized(self, tg_user: TgUser, msg: Message):
        self.tg_client.send_message(chat_id=msg.chat.id, text=f'Hello, {tg_user.user.username}!')


    def handle_unauthorized(self, tg_user: TgUser, msg: Message):
        """Генерируем, назначаем код юзеру и сохраним юзера в базе"""
        code = tg_user.gen_verification_code()
        tg_user.verification_code = code
        tg_user.save()

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'Hello! Your verification code: {code}'
        )

