from rest_framework import serializers

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    tg_chat_id = serializers.SlugField(source='chat_id', read_only=True)

    class Meta:
        model = TgUser
        fields = ('tg_chat_id', 'user', 'verification_code', 'tg_user_id')
        read_only_fields = ('tg_chat_id', 'user', 'tg_user_id')


