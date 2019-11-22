from django.contrib import admin
from django.db import models
from oauth2client.contrib.django_util.models import CredentialsField
from src.users.models import User


class CredentialsModel(models.Model):
    id = models.OneToOneField(User, primary_key=True,
                              on_delete=models.CASCADE)
    credential = CredentialsField()
