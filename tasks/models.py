from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField('Название категории', max_length=180, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        HIGH = "high"  # , ("high")
        MEDIUM = "mid"  # , ("mid")
        LOW = "low"  # , ("low")
    # LOW = 'low'
    # MID = 'mid'
    # HIGH = 'high'
    # PRIORITY_CHOICES = (
    #     (LOW, 'low'),
    #     (MID, 'mid'),
    #     (HIGH, 'high'),
    # )

    title = models.CharField('Заголовок задачи', max_length=150)
    description = models.TextField('Описание задачи')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name='Автор задачи',
        null=True
    )
    performer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks_to_do',
        verbose_name='Мои задачи',
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='tasks',
        null=True,
    )
    priority = models.CharField(
        choices=Priority.choices,  # PRIORITY_CHOICES,
        default='low',
        verbose_name='Приоритет',
        max_length=10  #max(
        #     map(len, [priority for priority, _ in PRIORITY_CHOICES])
        # )
    )

    is_subtask = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    creation_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        verbose_name='Дата обновления',
        auto_now=True
    )
    complete_date = models.DateTimeField(
        verbose_name='Дата выполнения',
        null=True,
        blank=True,
        # auto_now=True
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-update_date']

    def __str__(self):
        return self.title


class TaskSubtask(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='task',
        verbose_name='Задача'
    )
    subtask = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='subtasks',
        verbose_name='Подзадача'
    )

    class Meta:
        verbose_name = 'Задачи/Подзадачи'
        verbose_name_plural = 'Задачи/Подзадачи'

    def __str__(self):
        return f'{self.task} - {self.subtask}'


# class Subtask(Task):

#     task = models.ForeignKey(
#         Task,
#         on_delete=models.CASCADE,
#         related_name='subtasks',
#         verbose_name='Подзадачи'
#     )
#     # is_subtask = models.BooleanField(default=True)

#     class Meta:
#         verbose_name = 'Подзадача'
#         verbose_name_plural = 'Подзадачи'
#         ordering = ('id',)

#     def __str__(self):
#         return self.id
