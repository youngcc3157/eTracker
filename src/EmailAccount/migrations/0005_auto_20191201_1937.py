# Generated by Django 2.2.6 on 2019-12-02 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmailAccount', '0004_gmailcredential'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CheckedEmail',
            new_name='CheckedMessage',
        ),
        migrations.RenameField(
            model_name='checkedmessage',
            old_name='email_id',
            new_name='message_id',
        ),
    ]
