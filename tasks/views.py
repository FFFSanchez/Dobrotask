from datetime import timedelta

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import TaskPriorityFilter, TaskPriorityOrderingFilter
from .models import Category, Task, TaskSubtask
from .permissions import IsAdminOrAuthorOrPerformerOrReadOnly
from .serializers import (CategorySerializer, CategoryStatisticsSerializer,
                          MyTasksSerializer, TaskSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    """ All operations with tasks """

    queryset = Task.objects.exclude(is_subtask=True)
    serializer_class = TaskSerializer
    permission_classes = (IsAdminOrAuthorOrPerformerOrReadOnly,)

    filter_backends = (DjangoFilterBackend, TaskPriorityOrderingFilter,)
    filterset_fields = ('priority',)
    filterset_class = TaskPriorityFilter
    ordering_fields = ('priority',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, performer=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = Task.objects.all()
        instance = self.get_object()
        serializer = TaskSerializer(instance)
        return Response(serializer.data)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        methods=['get']
    )
    def my_tasks_to_do(self, request):
        queryset = request.user.tasks_to_do.all()
        qs_priority_filtered = self.filter_queryset(queryset)
        serializer = MyTasksSerializer(qs_priority_filtered, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        methods=['get']
    )
    def my_tasks_created_by_me(self, request):
        queryset = request.user.created_tasks.all()
        qs_priority_filtered = self.filter_queryset(queryset)
        serializer = MyTasksSerializer(qs_priority_filtered, many=True)
        return Response(serializer.data)

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def add_subtask(self, request, pk):
        task = get_object_or_404(Task, id=pk)
        if task.performer == request.user or task.author == request.user:
            serializer = TaskSerializer(
                data=request.data
            )
            serializer.is_valid(raise_exception=True)
            subtask = serializer.save(
                author=self.request.user,
                performer=self.request.user,
                is_subtask=True
            )

            TaskSubtask.objects.create(task=task, subtask=subtask)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {
                "task": "Only author or performer of task can create subtasks!"
            },
            status=status.HTTP_403_FORBIDDEN
        )

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def complete_task(self, request, pk):
        task = get_object_or_404(Task, id=pk)
        if task.performer == request.user or task.author == request.user:
            task.completed = True
            task.complete_date = timezone.now()
            task.spent_time_for_complete = (
                task.complete_date - task.creation_date
            ).seconds
            task_id = task.id
            task.save()

            return Response(
                {f"task with id {task_id}": "completed"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"task": "You are not author or performer in this task!"},
                status=status.HTTP_403_FORBIDDEN
            )

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def my_tasks_statistics(self, request):
        """ Statistics for my tasks """

        qs_author = request.user.created_tasks.all()
        qs_performer = request.user.tasks_to_do.all()

        completed_by_me = qs_performer.filter(completed=True)

        avg_completion_time_formated = "You have not completed tasks"
        if completed_by_me.exists():
            avg_completion_time = completed_by_me.aggregate(
                Avg('spent_time_for_complete')
            ).get('spent_time_for_complete__avg')
            avg_completion_time_formated = str(
                timedelta(seconds=avg_completion_time)
            )

        summary = {
            "tasks created by me": len(qs_author),
            "tasks to do": len(qs_performer),
            "completed by me": len(completed_by_me),
            "completed at all": len(qs_author.filter(completed=True)),
            "not completed": len(qs_performer.filter(completed=False)),
            "avg completion time": avg_completion_time_formated
        }
        return Response(summary, status=status.HTTP_200_OK)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def category_statistics(self, request):

        categories_qs = Category.objects.all()

        serializer = CategoryStatisticsSerializer(categories_qs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
