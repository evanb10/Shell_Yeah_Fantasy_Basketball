# Generated by Django 4.2.13 on 2024-10-31 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lottery_sim', '0008_roster'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='league_id',
            field=models.CharField(default=0, max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='manager',
            unique_together={('manager_id', 'league_id')},
        ),
    ]