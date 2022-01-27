from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from api_yamdb.settings import PROJECT_SETTINGS


class CustomUserManager(UserManager):
    def create_superuser(
            self,
            email,
            username,
            role='user',
            bio=None,
            password=None
    ):
        user = self.create_user(
            email=email,
            username=username,
            is_staff=True,
            is_superuser=True,
        )
        user.is_admin = True
        user.role = PROJECT_SETTINGS['role']['admin']
        user.set_password(password)
        user.confirmation_code = make_password(
            '00000', salt=None, hasher='argon2'
        )
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    email = models.EmailField(
        help_text='email address',
        blank=False,
        unique=True
    )
    bio = models.TextField(max_length=1000, blank=True)
    is_admin = models.BooleanField(default=False)
    confirmation_code = models.CharField(
        max_length=200,
        default=None,
        blank=True,
        null=True
    )

    ROLE_CHOICE = [
        PROJECT_SETTINGS['role']['user'],
        PROJECT_SETTINGS['role']['moderator'],
        PROJECT_SETTINGS['role']['admin'],
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICE,
        default=PROJECT_SETTINGS['role']['user'][0]
    )

    @property
    def is_administrator(self):
        return (self.role == self.ROLE_CHOICE[2][0]
                or self.is_superuser)

    @property
    def is_moderator(self):
        return self.role == self.ROLE_CHOICE[1][0]

    objects = CustomUserManager()
