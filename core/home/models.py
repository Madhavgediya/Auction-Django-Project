from django.db import models

# Create your models here.

class Categorie(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.category_name

class Product(models.Model):
    products_name = models.CharField(max_length=255)
    products_base_price = models.IntegerField()
    product_category = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True) 
    product_description = models.CharField(max_length=255, default='No Description Available')
    product_image = models.ImageField(upload_to='', null=True, blank=True)  # Add this line for the image field
    def __str__(self):
        return self.products_name 


class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128)  # Note: In a real-world scenario, you'd use a more secure way to store passwords

    def __str__(self):
        return self.username
    