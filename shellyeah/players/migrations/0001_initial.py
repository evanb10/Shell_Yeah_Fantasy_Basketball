# Generated by Django 4.2.13 on 2024-10-30 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_id', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(default='N/A', max_length=100)),
                ('last_name', models.CharField(default='N/A', max_length=100)),
                ('team', models.CharField(max_length=50, null=True)),
                ('age', models.IntegerField(default=0)),
                ('position', models.CharField(default='N/A', max_length=10)),
                ('weight', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
            ],
        ),
    ]