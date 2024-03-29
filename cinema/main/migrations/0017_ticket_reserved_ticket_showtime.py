# Generated by Django 4.0.3 on 2022-04-27 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_remove_ticket_ticket_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='reserved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='showtime',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.showtime'),
        ),
    ]
