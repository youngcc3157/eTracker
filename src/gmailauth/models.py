from django.contrib import admin
from django.db import models
from oauth2client.contrib.django_util.models import CredentialsField
from src.EmailAccount.models import EmailAccount


class CredentialsModel(models.Model):
    id = models.OneToOneField(EmailAccount, primary_key=True,
                              on_delete=models.CASCADE)
    credential = CredentialsField()
