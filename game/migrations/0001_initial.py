# Generated by Django 5.0.6 on 2024-06-05 08:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('player', '0001_initial'),
        ('tournament', '0002_tournament_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games_as_one', to='player.player')),
                ('player_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games_as_two', to='player.player')),
                ('tournament', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='games', to='tournament.tournament')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wins', to='player.player')),
            ],
        ),
    ]
