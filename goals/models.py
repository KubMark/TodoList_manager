from django.db import models
from django.utils import timezone

from core.models import User


class DateModel(models.Model):
    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class GoalCategory(DateModel):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT, related_name='goal_category')
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    def __str__(self) -> str:
        return self.title


class Goal(DateModel):
    class Status(models.IntegerChoices):
        to_do = 1, 'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнено'
        archived = 4, 'Архив'

    class Priority(models.IntegerChoices):
        low = 1, 'Низкий'
        medium = 2, 'Средний'
        high = 3, 'Высокий'
        critical = 4, 'Критический'

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    category = models.ForeignKey(GoalCategory, on_delete=models.PROTECT, verbose_name='Категория')

    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.to_do, verbose_name='Статус')
    priority = models.PositiveSmallIntegerField(choices=Priority.choices, default=Priority.medium, verbose_name='Приоритет')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор')
    due_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата дедлайна')

    def __str__(self):
        return self.title


class GoalComment(DateModel):
    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    goal = models.ForeignKey(Goal, verbose_name='Цель', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return self.text
