# Generated by Django 4.2.13 on 2024-06-06 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0002_tournament_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournament',
            old_name='type',
            new_name='category',
        ),
        migrations.AddField(
            model_name='tournament',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tournament',
            name='tournament_type',
            field=models.CharField(choices=[('RONDE', 'Rondes'), ('CLASSIC', 'Classique')], default='CLASSIC', max_length=100),
        ),
    ]
