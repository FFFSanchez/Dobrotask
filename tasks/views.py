from rest_framework import status, viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import Task, Category, TaskSubtask
from .serializers import (
    CategorySerializer, TaskSerializer, MyTasksSerializer
)
from django.utils import timezone
# from django.db.models import Sum
from .filters import TaskPriorityFilter, TaskPriorityOrderingFilter
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from .permissions import IsAdminOrAuthorOrPerformerOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    # queryset = Task.objects.all()
    queryset = Task.objects.exclude(is_subtask=True) #(subtasks.all() # .exists()
    serializer_class = TaskSerializer
    permission_classes = (IsAdminOrAuthorOrPerformerOrReadOnly,)

    filter_backends = (DjangoFilterBackend, TaskPriorityOrderingFilter,) # filters.OrderingFilter)
    filterset_fields = ('priority',)
    filterset_class = TaskPriorityFilter
    ordering_fields = ('priority',)
    # ordering = ('priority',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, performer=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        print('ret')
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
        # print(request.user.tasks_to_do.all())
        queryset = request.user.tasks_to_do.all()
        qs_priority_filtered = self.filter_queryset(queryset)
        # serializer = self.get_serializer(request.user.tasks_to_do.all(), many=True)
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
        serializer = TaskSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)  # show msg task field is required
        subtask = serializer.save(
            author=self.request.user,
            performer=self.request.user,
            is_subtask=True
        )

        TaskSubtask.objects.create(task=task, subtask=subtask)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
            task_id = task.id
            task.save()

            return Response({f"task with id {task_id}": "completed"}, status=status.HTTP_200_OK)
        else:
            return Response({"task": "You dont have rights!"}, status=status.HTTP_403_FORBIDDEN)
