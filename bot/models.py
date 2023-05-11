from django.db import models

from core.models import User


class TgUser(models.Model):
    class Meta:
        verbose_name = 'Телеграм-пользователь'
        verbose_name_plural = 'Телеграм-пользователи'

    chat_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    verification_code = models.CharField(max_length=50, default=None, null=True, blank=True)
