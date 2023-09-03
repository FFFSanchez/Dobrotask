from datetime import timedelta

from django.db.models import Avg, F
from rest_framework import serializers

from users.models import User

from .models import Category, Task


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryStatisticsSerializer(serializers.ModelSerializer):
    """ Statistics for categories """

    tasks_amount = serializers.SerializerMethodField()
    tasks_completed = serializers.SerializerMethodField()
    tasks_in_progress = serializers.SerializerMethodField()
    tasks_author_not_performer = serializers.SerializerMethodField()
    average_tasks_completion_time = serializers.SerializerMethodField()

    def get_tasks_amount(self, obj):
        tasks_amount = obj.tasks.count()
        return tasks_amount

    def get_tasks_completed(self, obj):
        tasks_completed = obj.tasks.filter(completed=True).count()
        return tasks_completed

    def get_tasks_in_progress(self, obj):
        tasks_in_progress = obj.tasks.filter(completed=False).count()
        return tasks_in_progress

    def get_tasks_author_not_performer(self, obj):
        tasks_author_not_performer = obj.tasks.exclude(
            author__in=F('performer')
        ).count()
        return tasks_author_not_performer

    def get_average_tasks_completion_time(self, obj):
        tasks_completed = obj.tasks.filter(completed=True)

        if tasks_completed.exists():
            avg_completion_time = tasks_completed.aggregate(
                Avg('spent_time_for_complete')
            ).get('spent_time_for_complete__avg')
            avg_completion_time_formated = str(
                timedelta(seconds=avg_completion_time)
            )

            return avg_completion_time_formated
        return "No completed tasks in this category"

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'tasks_amount',
            'tasks_completed',
            'tasks_in_progress',
            'tasks_author_not_performer',
            'average_tasks_completion_time'
        )


class ShortTaskSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    performer = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    subtasks = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )

    def get_subtasks(self, obj):
        queryset = Task.objects.filter(subtasks__in=obj.task.all())
        return ShortTaskSerializer(queryset, many=True).data

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'priority',
            'performer',
            'author',
            'category',
            'subtasks'
        )


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    performer = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all(), required=False
    )
    subtasks = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all(), required=False
    )

    def get_subtasks(self, obj):
        queryset = Task.objects.filter(subtasks__in=obj.task.all())

        return ShortTaskSerializer(queryset, many=True).data

    class Meta:
        model = Task
        exclude = ('is_subtask', 'spent_time_for_complete')


class MyTasksSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    main_task = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all()
    )

    def get_main_task(self, obj):
        if obj.subtasks.all().exists():
            task = Task.objects.get(id=obj.subtasks.all().values_list()[0][1])
            return f'{task.title}, id: {task.id}'
        else:
            return 'This is main task'

    class Meta:
        model = Task
        exclude = ('performer', 'spent_time_for_complete')
