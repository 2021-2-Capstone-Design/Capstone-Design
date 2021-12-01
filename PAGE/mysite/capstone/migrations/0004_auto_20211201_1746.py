# Generated by Django 3.1.3 on 2021-12-01 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0003_auto_20211128_2034'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playerName', models.CharField(max_length=20)),
                ('user_id', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='record',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='record',
            name='create_date',
        ),
        migrations.RemoveField(
            model_name='record',
            name='playerName',
        ),
        migrations.DeleteModel(
            name='PlayerName',
        ),
    ]