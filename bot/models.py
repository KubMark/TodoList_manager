from django.db import models
from core.models import User


class TgUser(models.Model):
    telegram_chat_id = models.CharField(verbose_name='tg chat id', unique=True, max_length=80)
    telegram_user_id = models.CharField(verbose_name='tg user id', unique=True, max_length=80)
    user = models.ForeignKey(User, verbose_name='Автор', null=True, blank=True, on_delete=models.CASCADE)
    verification_code = models.CharField(max_lenght=100, null=True, blank=True)
