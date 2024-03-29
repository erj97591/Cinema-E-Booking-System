# Generated by Django 4.0.3 on 2022-04-27 03:04

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_booking_showtime_showtime_slug_alter_showtime_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showtime',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from=['movie', 'date', 'time']),
        ),
    ]
