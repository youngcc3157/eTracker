# Generated by Django 2.2.6 on 2019-12-02 00:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmailAccount', '0005_auto_20191201_1937'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkedmessage',
            old_name='email_account',
            new_name='email_account_id',
        ),
    ]
