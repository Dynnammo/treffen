# Generated by Django 3.2.4 on 2021-06-18 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treffen', '0002_alter_player_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
