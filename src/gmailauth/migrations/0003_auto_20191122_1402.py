# Generated by Django 2.2.6 on 2019-11-22 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gmailauth', '0002_auto_20191122_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credentialsmodel',
            name='id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='EmailAccount.EmailAccount'),
        ),
    ]
