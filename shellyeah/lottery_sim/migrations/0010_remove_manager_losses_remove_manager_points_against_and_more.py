# Generated by Django 4.2.13 on 2024-11-01 02:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lottery_sim', '0009_manager_league_id_alter_manager_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manager',
            name='losses',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='points_against',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='points_for',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='record',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='wins',
        ),
    ]
