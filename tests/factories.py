import factory
from django.utils import timezone
from pytest_factoryboy import register

from core.models import User
from goals.models import Board, BoardParticipant, GoalCategory, Goal, GoalComment


@register
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):

        return User.objects.create_user(*args, **kwargs)


class DatesFactoryMixin(factory.django.DjangoModelFactory):
    created = factory.LazyFunction(timezone.now)
    updated = factory.LazyFunction(timezone.now)

    class Meta:
        abstract = True


@register
class BoardFactory(DatesFactoryMixin):
    title = factory.Faker('sentence')

    class Meta:
        model = Board

    @factory.post_generation
    def with_owner(self, create, owner, **kwargs):
        if owner:
            BoardParticipant.objects.create(board=self, user=owner, role=BoardParticipant.Role.owner)

@register
class CategoryFactory(DatesFactoryMixin):
    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence')
    board = factory.SubFactory(BoardFactory)

    class Meta:
        model = GoalCategory


@register
class GoalFactory(DatesFactoryMixin):
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    title = factory.Faker('sentence')

    class Meta:
        model = Goal


@register
class GoalCommentFactory(DatesFactoryMixin):
    goal = factory.SubFactory(GoalFactory)
    user = factory.SubFactory(UserFactory)
    text = factory.Faker('sentence')

    class Meta:
        model = GoalComment
