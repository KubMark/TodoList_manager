import pytest
from django.urls import reverse
from rest_framework import status
from goals.serializers import BoardCreateSerializer


@pytest.mark.django_db
class TestBoardsList:
    url = reverse('board-list')

    def test_get_list_unauthorized(self, client):
        """
        Unauthorized user get an error when requesting a list of boards
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_list_of_boards_not_participant(self, auth_client, board_factory):
        """
        If authorized user is not a member of any board will receive an empty list
        """
        board_factory.create_batch(size=2)
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_get_list_success(self, auth_client, board_factory, user):
        """
        Authorized user receives a list of boards in which he is a member
        """
        boards = board_factory.create_batch(size=2, with_owner=user)
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        for board in BoardCreateSerializer(boards, many=True).data:
            assert board in response.data
