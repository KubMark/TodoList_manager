from unittest.mock import ANY
import pytest
from django.urls import reverse
from rest_framework import status
from goals.models import GoalCategory


@pytest.mark.django_db
class TestCategoryCreateView:
    url = reverse('create-category')

    def test_create_unauthorized(self, client, faker):
        """
        When creating Category Unauthorized user gets Unauthorized error
        """
        k = faker.pydict(1)
        response = client.post(self.url, data={})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_without_board(self, auth_client):
        """
        При создании категории целей авторизованный пользователь не передает параметром доску и получает ошибку
        When creating
        """
        response = auth_client.post(self.url, data={
            'title': 'Category',
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_success(self, auth_client, board) -> None:
        """
        Авторизованный пользователь успешно создает категорию целей
        """
        board, _ = board
        response = auth_client.post(self.url, data={
            'title': 'Category',
            'board': board.id
        })
        category = GoalCategory.objects.last()
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            'id': category.id,
            'created': ANY,
            'updated': ANY,
            'title': category.title,
            'is_deleted': category.is_deleted,
            'board': category.board.id
        }