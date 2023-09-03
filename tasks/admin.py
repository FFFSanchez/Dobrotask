from django.contrib import admin

from .models import Category, Task, TaskSubtask


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'performer',
        'category',
        'priority',
        'completed'
    )
    search_fields = ('category',)
    list_filter = ('priority',)
    list_display_links = ('title',)
    empty_value_display = '-xxx-'


class TaskSubtaskAdmin(admin.ModelAdmin):
    list_display = (
        'task',
        'subtask'
    )
    empty_value_display = '-xxx-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )
    list_display_links = ('name',)
    empty_value_display = '-xxx-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(TaskSubtask, TaskSubtaskAdmin)
admin.site.register(Task, TaskAdmin)
