from django.contrib import admin
from django.db import models
from oauth2client.contrib.django_util.models import CredentialsField


class EmailAccount(models.Model):
    email = models.EmailField(max_length=254)
    email_type = models.CharField(max_length=254)


class CheckedEmail(models.Model):
    email_id = models.CharField(max_length=100, primary_key=True)
    email_account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE)


class GmailCredential(models.Model):
    id = models.OneToOneField(EmailAccount, primary_key=True,
                              on_delete=models.CASCADE)
    credential = CredentialsField()
