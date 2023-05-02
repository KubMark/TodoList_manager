from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from goals.models import GoalComment
from goals.permissions import CommentPermissions
from goals.serializers import GoalCommentSerializer, GoalCommentCreateSerializer

# Comments


class CommentCreateView(CreateAPIView):
    queryset = GoalComment.objects.all()
    serializer_class = GoalCommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated, CommentPermissions]


class CommentListView(ListAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('goal', )
    ordering = ('-created', )

    def get_queryset(self) -> QuerySet[GoalComment]:
        return GoalComment.objects.select_related('user').filter(user_id=self.request.user.id)


class CommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated, CommentPermissions]

    def get_queryset(self) -> QuerySet[GoalComment]:
        return GoalComment.objects.select_related('user').filter(user_id=self.request.user.id)
