# Generated by Django 4.2.13 on 2024-07-22 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pool', '0005_remove_pool_games'),
        ('game', '0003_alter_game_tournament'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='pool',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games', to='pool.pool'),
        ),
    ]