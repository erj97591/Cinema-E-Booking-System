# Generated by Django 4.0.3 on 2022-04-13 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_movie_promotion_showroom_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showtime',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='showtimes', to='main.movie'),
        ),
    ]
