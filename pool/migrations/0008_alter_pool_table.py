# Generated by Django 4.2.13 on 2024-08-14 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pool', '0007_pool_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pool',
            name='table',
            field=models.TextField(null=True),
        ),
    ]
