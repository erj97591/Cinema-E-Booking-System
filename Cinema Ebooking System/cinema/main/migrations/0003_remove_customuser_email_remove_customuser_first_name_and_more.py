# Generated by Django 4.0.3 on 2022-03-22 01:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_customuser_paymentcard_delete_custom_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='last_name',
        ),
    ]
