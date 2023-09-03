import django_filters
from django.db.models import Case, Value, When
from rest_framework.filters import OrderingFilter

from .models import Task


class TaskPriorityOrderingFilter(OrderingFilter):
    """ Ordering by priority values """
    def filter_queryset(self, request, queryset, view):

        ordering = request.GET.get('ordering')
        if ordering == 'priority':
            priority_order = Case(
                When(priority=Task.Priority.HIGH, then=Value(1)),
                When(priority=Task.Priority.MEDIUM, then=Value(2)),
                When(priority=Task.Priority.LOW, then=Value(3)),
            )
            ordered = queryset.alias(
                priority_order=priority_order
            ).order_by("priority_order",)
            print('ORD', ordered)
            return ordered
        return queryset


class TaskPriorityFilter(django_filters.FilterSet):
    """ Filter by priority values """
    class Meta:
        model = Task
        fields = ("priority", )
