import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestGoalsListView:
    url = reverse('goal-list')

    def test_get_list_unauthorized(self, client) -> None:
        """
         Non authorized user gets an error when requests Goal list
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

