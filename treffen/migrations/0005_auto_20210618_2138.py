# Generated by Django 3.2.4 on 2021-06-18 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treffen', '0004_game_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('WTS', 'Waiting to start'), ('S', 'Started'), ('P', 'Paused'), ('O', 'Over')], default='W', max_length=20),
        ),
        migrations.AlterField(
            model_name='game',
            name='type',
            field=models.CharField(choices=[('BR', 'Battle Royale'), ('CO', 'Cooperation'), ('CH', 'Championship')], default='BR', max_length=20),
        ),
    ]
