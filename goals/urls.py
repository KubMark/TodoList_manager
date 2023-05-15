from django.urls import path

from goals.views import category, comment, goals, board

urlpatterns = [
    # Boards
    path("board/create", board.BoardCreateView.as_view(), name='create-board'),
    path("board/list", board.BoardListView.as_view(), name='board-list'),
    path("board/<pk>", board.BoardView.as_view(), name='board'),
    # Goal categories
    path("goal_category/create", category.GoalCategoryCreateView.as_view(), name='create-category'),
    path("goal_category/list", category.GoalCategoryListView.as_view(), name='category-list'),
    path("goal_category/<pk>", category.GoalCategoryView.as_view(), name='category'),
    # Goals
    path("goal/create", goals.GoalCreateView.as_view(), name='create-goal'),
    path("goal/list", goals.GoalListView.as_view(), name='goal-list'),
    path("goal/<pk>", goals.GoalView.as_view(), name='goal'),
    # Goal Comments
    path("goal_comment/create", comment.CommentCreateView.as_view(), name='create-comment'),
    path("goal_comment/list", comment.CommentListView.as_view(), name='comment-list'),
    path("goal_comment/<pk>", comment.CommentView.as_view(), name='comment'),

]
