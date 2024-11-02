# Generated by Django 4.2.13 on 2024-10-31 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0002_alter_player_age_alter_player_position'),
        ('lottery_sim', '0007_leaguemembership'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_id', models.ForeignKey(db_column='manager_id', on_delete=django.db.models.deletion.CASCADE, to='lottery_sim.manager')),
                ('player_id', models.ForeignKey(db_column='player_id', on_delete=django.db.models.deletion.CASCADE, to='players.player')),
            ],
        ),
    ]
