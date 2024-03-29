# Generated by Django 4.0.3 on 2022-04-16 21:37

import datetime
from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_showtime_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='trailer',
            field=embed_video.fields.EmbedVideoField(),
        ),
        migrations.AlterField(
            model_name='showtime',
            name='date',
            field=models.DateField(default=datetime.date(2022, 4, 16)),
        ),
    ]
