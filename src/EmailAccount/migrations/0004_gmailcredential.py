# Generated by Django 2.2.6 on 2019-11-27 04:25

from django.db import migrations, models
import django.db.models.deletion
import oauth2client.contrib.django_util.models


class Migration(migrations.Migration):

    dependencies = [
        ('EmailAccount', '0003_checkedemail'),
    ]

    operations = [
        migrations.CreateModel(
            name='GmailCredential',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='EmailAccount.EmailAccount')),
                ('credential', oauth2client.contrib.django_util.models.CredentialsField(null=True)),
            ],
        ),
    ]