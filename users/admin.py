from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'is_admin',
        'is_active',
        'date_joined'
    )
    search_fields = ('username',)
    list_display_links = ('username',)
    list_filter = ('is_admin', 'email', 'username')
    empty_value_display = '-xxx-'


admin.site.register(User, UserAdmin)
