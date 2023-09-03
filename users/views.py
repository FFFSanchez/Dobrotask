from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User

# from .filters import TitleFilter
from .permissions import (
    IsAdmin,
    # IsAdminOrModeratorOrAuthorOrReadOnly,
    # IsAdminOrReadOnly,
)
from .serializers import (
    # CategorySerializer,
    # CommentSerializer,
    # GenreSerializer,
    MeSerializer,
    # RegisterDataSerializer,
    # ReviewSerializer,
    # TitleSerializerGet,
    # TitleSerializerPost,
    # TokenSerializer,
    UserSerializer,
)


# @api_view(['POST'])
# @permission_classes([permissions.AllowAny])
# def register(request):
#     """Функция для регистрации новых пользователей"""

#     serializer = RegisterDataSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)

#     user = serializer.save()
#     confirmation_code = default_token_generator.make_token(user)
#     send_mail(
#         subject='YaMDB registration',
#         message=f'Confirmation code: {confirmation_code}',
#         from_email=settings.TOKEN_EMAIL,
#         recipient_list=[user.email],
#     )
#     return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([permissions.AllowAny])
# def get_jwt_token(request):
#     serializer = TokenSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = get_object_or_404(
#         User,
#         username=serializer.validated_data['username'],
#     )
#     if default_token_generator.check_token(
#         user, serializer.validated_data['confirmation_code']
#     ):
#         token = AccessToken.for_user(user)
#         return Response({'token': str(token)})
#     return Response(
#         {'confirmation_code': ['неверный код подтверждения']},
#         status=status.HTTP_400_BAD_REQUEST,
#     )


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     # permission_classes = (IsAdmin,)
#     lookup_field = 'username'
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('username',)
#     http_method_names = ['get', 'post', 'patch', 'delete']

#     @action(
#         detail=False,
#         permission_classes=(IsAuthenticated,),
#         methods=['get', 'patch'],
#     )
#     def me(self, request):
#         if request.method == 'PATCH':
#             serializer = MeSerializer(
#                 request.user, data=request.data, partial=True
#             )
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(data=serializer.data)
#         serializer = self.get_serializer(request.user)
#         return Response(serializer.data)
