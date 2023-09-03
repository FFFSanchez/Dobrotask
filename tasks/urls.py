from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, TaskViewSet

app_name = 'tasks'

router = DefaultRouter()

router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('', include(router.urls)),
]
