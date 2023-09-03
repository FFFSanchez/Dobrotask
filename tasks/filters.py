import django_filters
from django.db.models import Case, Value, When
from .models import Task
from rest_framework.filters import OrderingFilter


class TaskPriorityOrderingFilter(OrderingFilter):
    # def get_ordering(self, request, queryset, view):
    #     ordering = request.GET.get('ordering')
    #     print('QS2', queryset)
    #     if ordering == 'priority':
    #         priority_order = Case(
    #             When(priority=Task.Priority.HIGH, then=Value(1)),
    #             When(priority=Task.Priority.MEDIUM, then=Value(2)),
    #             When(priority=Task.Priority.LOW, then=Value(3)),
    #         )
    #         # ordered = Task.objects.alias(priority_order=priority_order).order_by("priority_order",)  # "title")
    #         ordered = queryset.alias(priority_order=priority_order).order_by("priority_order",)
    #         print('ORD2', ordered)
    #         return ordered  # queryset.order_by('priority', lambda x: )
    #     print('no ordering')
    #     return super().get_ordering(request, queryset, view)

    def filter_queryset(self, request, queryset, view):

        ordering = request.GET.get('ordering')
        print('QS', queryset)
        if ordering == 'priority':
            priority_order = Case(
                When(priority=Task.Priority.HIGH, then=Value(1)),
                When(priority=Task.Priority.MEDIUM, then=Value(2)),
                When(priority=Task.Priority.LOW, then=Value(3)),
            )
            # ordered = Task.objects.alias(priority_order=priority_order).order_by("priority_order",)  # "title")
            ordered = queryset.alias(priority_order=priority_order).order_by("priority_order",)
            print('ORD', ordered)
            return ordered
        return queryset


class TaskPriorityFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ("priority", )


#  PRIORITY_ORDER = {
#                 Todo.Priority.HIGH: 1,
#                 Todo.Priority.MEDIUM: 2,
#                 Todo.Priority.LOW: 3,
#             }
#             sorted(
#                 Todo.objects.all(),
#                 key=lambda x: [PRIORITY_ORDER[x.priority], x.title],
#             )