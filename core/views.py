from django.contrib.auth import login
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from core.models import User
from core.serializers import CreateUserSerializer, LoginSerializer


class CreateAccountView(CreateAPIView):
    """ Ручка регистрации нового пользователя """
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs) -> Response:
        serializer: LoginSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer) -> None:
        """ Происходит логин через cookies"""
        user: User = serializer.save()
        login(request=self.request, user=user)
