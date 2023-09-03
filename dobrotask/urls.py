from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('', include('users.urls', namespace='users')),
        path('', include('tasks.urls', namespace='tasks'))
    ]))
]

schema_view = get_schema_view(
    openapi.Info(
        title="Refs API by Trifonov",
        default_version='v1',
        description="Docs for Refs Api App",
        contact=openapi.Contact(email="lordsanchez@yandex.ru"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]
