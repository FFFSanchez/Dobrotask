from rest_framework import serializers
from .models import Task, Category
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


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
        fields = ('id', 'title', 'priority', 'performer', 'author', 'category', 'subtasks')


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    performer = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all(), required=False
    )
    subtasks = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all()
    )

    def get_subtasks(self, obj):
        # print(obj)
        # print('d', obj.task.all())
        # print('d', obj.task.all().values())
        # print('d', list(obj.task.all().values()))
        # print('dss', obj.subtasks.all())

        queryset = Task.objects.filter(subtasks__in=obj.task.all())
        print('s', queryset)

        return ShortTaskSerializer(queryset, many=True).data

    class Meta:
        model = Task
        exclude = ('is_subtask', )


class MyTasksSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    main_task = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all()
    )

    def get_main_task(self, obj):
        print(f'obj {obj}')
        if obj.subtasks.all().exists():
            # print(f'subs {obj.subtasks.all()}')
            # print(f'main id: {obj.subtasks.all().values_list()[0][1]}')
            print('task is subtask')
            task = Task.objects.get(id=obj.subtasks.all().values_list()[0][1])
            return f'{task.title}, id: {task.id}'  # TaskSerializer(queryset, many=False).data
        else:
            print('task is not subtask')
            return 'This is main task'

    class Meta:
        model = Task
        exclude = ('performer', )
