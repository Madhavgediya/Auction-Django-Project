# Generated by Django 5.0 on 2024-02-03 05:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='auction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='home.auction'),
        ),
    ]
