# Generated by Django 3.1.3 on 2021-11-28 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0002_playername'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='playerName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capstone.playername'),
        ),
    ]
