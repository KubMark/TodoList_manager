from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer


# Category

class GoalCategoryCreateView(CreateAPIView):
    queryset = GoalCategory.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    queryset = GoalCategory.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ('title', 'created')
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(user=self.request.user, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    queryset = GoalCategory.objects.all()
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory) -> GoalCategory:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
        return instance


# Goal
class GoalCreateView(CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalListView(ListAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filter_class = GoalDateFilter
    ordering_fields = ('title', 'created')
    ordering = ['title']
    search_fields = ('title', 'description')

    def get_queryset(self):
        return Goal.objects.select_related('user').filter(
            user=self.request.user, category__is_deleted=False
        ).exclude(status=Goal.Status.archived)


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.select_related('user').filter(
            user=self.request.user, category__is_deleted=False
        ).exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save()
        return instance
