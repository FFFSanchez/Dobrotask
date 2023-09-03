from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import TaskViewSet, CategoryViewSet

app_name = 'tasks'

router = DefaultRouter()

# through djoser can be
# router.register(r'users', UserViewSet, basename='users')
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'categories', CategoryViewSet, basename='categories')
# router.register(r'tags', TagViewSet, basename='tags')
# router.register(r'ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [

    # path('users/', include('users.urls', namespace='users')),
    # path(
    #         'users/subscriptions/', SubscriptionsView.as_view(),
    #         name='subscriptions'
    #     ),
    # path('', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
