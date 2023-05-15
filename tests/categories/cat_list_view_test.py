import pytest
from django.urls import reverse
from rest_framework import status
from goals.serializers import GoalCategorySerializer


@pytest.mark.django_db
class TestCategoryList:
    url = reverse('category-list')

    def test_get_list_unauthorized(self, client):
        """
        Non authorized user gets an error when requests category list
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_list(self, auth_client, board, category_factory):
        """
        Authorized user gets category list
        """
        board, category = board
        categories = category_factory.create_batch(2, board=board)

        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        for category in GoalCategorySerializer(categories, many=True).data:
            assert category in response.data
