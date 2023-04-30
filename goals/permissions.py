from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from goals.models import GoalCategory, Goal, Board, GoalComment, BoardParticipant


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Board):

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user_id=request.user.id, board_id=obj).exists()
        return BoardParticipant.objects.filter(
            user_id=request.user.id, board_id=obj.id, role=BoardParticipant.Role.owner
        ).exists()


class CategoryPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request,  view: GenericAPIView, obj: GoalCategory) -> bool:
        return request.user == obj.user


class GoalPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request,  view: GenericAPIView, obj: Goal) -> bool:
        return request.user == obj.user


class CommentPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request,  view: GenericAPIView, obj: GoalComment) -> bool:
        return request.user == obj.user

