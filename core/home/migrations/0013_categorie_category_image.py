# Generated by Django 5.0 on 2024-02-07 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_bid_options_alter_bid_bid_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorie',
            name='category_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
