# Generated by Django 2.2.6 on 2019-11-22 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gmailauth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credentialsmodel',
            name='task',
        ),
        migrations.RemoveField(
            model_name='credentialsmodel',
            name='updated_time',
        ),
    ]