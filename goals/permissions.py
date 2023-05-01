from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from goals.models import GoalCategory, Goal, Board, GoalComment, BoardParticipant


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Board):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user_id=request.user.id, board_id=obj).exists()
        return BoardParticipant.objects.filter(
            user_id=request.user.id, board_id=obj.id,
            role=BoardParticipant.Role.owner).exists()


class CategoryPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: GoalCategory):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user_id=request.user.id, board_id=obj.board.id).exists()
        return BoardParticipant.objects.filter(
            user_id=request.user.id, board_id=obj.board.id,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()


class GoalPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: Goal) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user_id=request.user.id, board_id=obj.category.board.id).exists()
        return BoardParticipant.objects.filter(
            user_id=request.user.id, board_id=obj.category.board.id,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()


class CommentPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: GoalComment) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user_id=request.user.id, board_id=obj.goal.category.board.id).exists()
        return BoardParticipant.objects.filter(
            user_id=request.user.id, board_id=obj.goal.category.board.id,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()
