# Generated by Django 4.2.7 on 2023-12-20 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_customuser_delete_user_products_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
