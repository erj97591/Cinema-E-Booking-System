# Generated by Django 4.0.3 on 2022-04-27 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_booking_user_alter_booking_number_adult_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='ticket_type',
        ),
    ]
