import pytest
from rest_framework.test import APIClient

from goals.models import Board, GoalCategory, Goal, GoalComment
from tests.factories import BoardFactory, CategoryFactory, UserFactory, GoalFactory, GoalCommentFactory

pytest_plugins = 'tests.factories'


@pytest.fixture()
def client() -> APIClient:
    return APIClient()


@pytest.fixture()
def auth_client(client, user) -> APIClient:
    client.force_login(user)
    return client


@pytest.fixture
def board(board_factory: BoardFactory, category_factory: CategoryFactory, user: UserFactory) -> tuple[Board, GoalCategory]:
    board = board_factory.create(with_owner=user)
    category = category_factory.create(board=board, user=user)
    return board, category


@pytest.fixture
def goal(goal_factory: GoalFactory, user: UserFactory, board: tuple[Board, GoalCategory]) -> Goal:
    _, category = board
    return goal_factory.create(user=user, category=category)


@pytest.fixture
def comment(user: UserFactory, goal: GoalFactory, goal_comment_factory: GoalCommentFactory) -> GoalComment:
    return goal_comment_factory.create(user=user, goal=goal)