from django.contrib import admin
from bot.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('tg_chat_id', 'user')
    readonly_fields = ('verification_code', )
