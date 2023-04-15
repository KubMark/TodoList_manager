from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.models import User


class PasswordField(serializers.CharField):#
    def __init__(self, **kwargs):
        kwargs['style'] = {'input_type': 'password'}#   Добавится форма которая скрывает пароль
        kwargs.setdefault('write_only', True)
        super().__init__(**kwargs)#     Вызываем родителя и добавляем валидацию на пароль(они описаны в настройках)
        self.validators.append(validate_password)


class CreateUserSerializer(serializers.ModelSerializer):
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:# Проверяем что пароли совпадают
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError('Passwords must match')
        return attrs

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
