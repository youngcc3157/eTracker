# Generated by Django 2.2.6 on 2019-12-02 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EmailAccount', '0008_delete_checkedmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckedMessage',
            fields=[
                ('message_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('email_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmailAccount.EmailAccount')),
            ],
        ),
    ]