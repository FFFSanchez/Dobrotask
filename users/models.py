from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from rest_framework import status


class MyUserManager(BaseUserManager):
    def create(self, username, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(username=username,
                          email=self.normalize_email(email), **extra_fields
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):

        user = self.create(
            username,
            email,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(
        unique=True,
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='allows 150 characters or fewer @/./+/-/_ and digits',
                code=status.HTTP_400_BAD_REQUEST,
            ),
        ],
        blank=False
    )
    email = models.EmailField(max_length=254, unique=True, blank=False)
    password = models.CharField("password", max_length=128, blank=False)

    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def save(self, *args, **kwargs):
        if self.username == 'me':
            return ValidationError('Username не может быть "me".')
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username='me'),
                name='Пользователь не может быть назван me!',
            )
        ]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_short_name(self):
        return f'{self.username[:15]}'

    def __str__(self):
        return self.username
