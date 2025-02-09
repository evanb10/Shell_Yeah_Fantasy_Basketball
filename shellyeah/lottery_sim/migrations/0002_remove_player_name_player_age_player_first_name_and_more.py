# Generated by Django 4.2.13 on 2024-10-17 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lottery_sim', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='name',
        ),
        migrations.AddField(
            model_name='player',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='first_name',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AddField(
            model_name='player',
            name='height',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='last_name',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AddField(
            model_name='player',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(default='N/A', max_length=10),
        ),
        migrations.AlterField(
            model_name='player',
            name='team',
            field=models.CharField(default='N/A', max_length=50),
        ),
    ]
