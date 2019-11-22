from django.db import models
from django.contrib.auth.models import BaseUserManager, \
    AbstractBaseUser, \
    PermissionsMixin


class Board(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    class Meta:
        app_label = 'board'
