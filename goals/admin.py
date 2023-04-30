from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title',)
    list_filter = ('is_deleted', )
    readonly_fields = ('created', 'updated', )


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user', )
    list_filter = ('created', 'updated', )
    readonly_fields = ('created', 'updated', )


@admin.register(GoalComment)
class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', )
    list_filter = ('created', 'updated', )
    readonly_fields = ('created', 'updated', )

