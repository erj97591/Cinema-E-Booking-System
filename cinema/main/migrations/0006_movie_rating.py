# Generated by Django 4.0.3 on 2022-04-16 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_movie_trailer_alter_showtime_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='rating',
            field=models.CharField(default='G', max_length=100),
            preserve_default=False,
        ),
    ]
