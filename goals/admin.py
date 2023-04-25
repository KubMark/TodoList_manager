from django.contrib import admin

from goals.models import GoalCategory


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user', )
    list_filter = ('is_deleted', )
    readonly_fields = ('created', 'updated', )

