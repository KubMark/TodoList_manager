from uuid import uuid4

from django.db import models

from core.models import User


class TgUser(models.Model):
    class Meta:
        verbose_name = 'Телеграм-пользователь'
        verbose_name_plural = 'Телеграм-пользователи'

    chat_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    verification_code = models.CharField(max_length=50, default=None, null=True, blank=True)

    @staticmethod
    def _get_tg_user() -> str:
        return str(uuid4())

    def set_verification_code(self):
        code = self._get_tg_user()
        self.verification_code = code
        self.save(update_fields=('verification_code',))

        return code

