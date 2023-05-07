import os

from django.db import models
from core.models import User


class TgUser(models.Model):
    tg_chat_id = models.CharField(verbose_name='tg chat id', unique=True, max_length=80)
    tg_user_id = models.CharField(verbose_name='tg user id', unique=True, max_length=80)
    user = models.ForeignKey(User, verbose_name='Автор', null=True, blank=True, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=100, null=True, blank=True)

    def gen_verification_code(self):
        self.verification_code = os.urandom(16).hex()
        self.save(update_fields=('verification_code',))
        return self.verification_code
