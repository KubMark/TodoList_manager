from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory
from todolist import settings
import os

states = {}
cat_id = []

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.TELEGRAM_TOKEN)

    def handle(self, *args, **options):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1

                self.handle_message(item.message)

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(chat_id=msg.chat.id)
        if tg_user.user:
            self.handle_authorized(tg_user, msg)
        else:
            self.handle_unauthorized(tg_user, msg)

    def handle_authorized(self, tg_user: TgUser, msg: Message):
        allowed_commands = ['/goals', '/create', '/cancel']
        if '/goals' in msg.text:
            self.get_goals(msg, tg_user)

        elif '/create' in msg.text:
            self.handle_categories(msg, tg_user)

        elif '/cancel' in msg.text:
            self.get_cancel(tg_user)

        elif ('user' not in states) and (msg.text not in allowed_commands):
            self.tg_client.send_message(tg_user.chat_id, 'Command not found')

        elif (msg.text not in allowed_commands) and (states['user']) and \
                ('category' not in states):
            category = self.handle_save_category(tg_user, msg.text)
            if category:
                states['category'] = category
                self.tg_client.send_message(tg_user.chat_id,
                                            f'You choosed {category.title}, category, please enter name for your goal')
        elif (msg.text not in allowed_commands) and (states['user']) and \
                (states['category']) and ('goal_title' not in states):
            states['goal_title'] = msg.text
            goal = Goal.objects.create(title=states['goal_title'],
                                       user=states['user'],
                                       category=states['category'])
            self.tg_client.send_message(tg_user.chat_id, f'Your goal {goal} has been created')
            del states['user']
            del states['category']
            del states['goal_title']
            cat_id.clear()

    def handle_unauthorized(self, tg_user: TgUser, msg: Message):

        self.tg_client.send_message(msg.chat.id, 'Please confirm your account')
        code = os.urandom(12).hex()
        tg_user.verification_code = code
        tg_user.save(update_fields=['verification_code'])
        self.tg_client.send_message(tg_user.chat_id, f'Hello! Your verification code: {code}')

    def get_goals(self, msg: Message, tg_user: TgUser):
        goals = Goal.objects.filter(user=tg_user.user)
        if goals.count() > 0:
            response = [f'#{item.id} {item.title}' for item in goals]
            self.tg_client.send_message(msg.chat.id, '\n'.join(response))
        else:
            self.tg_client.send_message(msg.chat.id, 'Goals not found')

    def handle_categories(self, msg, tg_user: TgUser):
        categories = GoalCategory.objects.filter(user=tg_user.user, is_deleted=False)
        if categories.count() > 0:
            category_list = ''
            for cat in categories:
                category_list += f'{cat.id}: {cat.title} \n'
                cat_id.append(cat.id)
            self.tg_client.send_message(
                chat_id=tg_user.chat_id,
                text=f'Выберите номер категории для новой цели:\n{category_list}')
            if 'user' not in states:
                states['user'] = tg_user.user
        else:
            self.tg_client.send_message(msg.chat.id, 'No Categories found, first create category '
                                                     'on website for your goals')

    def handle_save_category(self, tg_user: TgUser, msg: str):
        category_id = int(msg)
        category_data = GoalCategory.objects.filter(user=tg_user.user).get(pk=category_id)
        return category_data

    def get_cancel(self, tg_user: TgUser):
        if 'user' in states:
            del states['user']
        if 'category' in states:
            del states['category']
        if 'goal_title' in states:
            del states['goal_title']
        self.tg_client.send_message(tg_user.chat_id, 'Operation canceled')
