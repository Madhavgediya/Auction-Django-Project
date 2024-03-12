from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.

class Categorie(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    category_image = models.ImageField(upload_to='', null=True, blank=True)  # Add this line for the image field
    def __str__(self):
        return self.category_name

class Product(models.Model):
    products_name = models.CharField(max_length=255)
    products_base_price = models.IntegerField()
    product_category = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True) 
    product_description = models.CharField(max_length=255, default='No Description Available')
    product_image = models.ImageField(upload_to='', null=True, blank=True)  # Add this line for the image field
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_products', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Set the created_by field to the currently logged-in user
        if not self.created_by_id and 'user' in kwargs:
            self.created_by = kwargs['user']
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.products_name 
    


class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128)  # Note: In a real-world scenario, you'd use a more secure way to store passwords

    def __str__(self):
        return self.username
    
class Auction(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    def __str__(self):
        return self.product.products_name if self.product else "No Product"
    
    def get_absolute_url(self):
        return reverse('auction_detail', args=[str(self.id)])
    
    def has_ended(self):
        return timezone.now() > self.end_time

class Bid(models.Model):
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.bid_amount}"
    
class Winner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.auction.product.products_name}'

    def get_absolute_url(self):
        return reverse('winner', args=[str(self.auction.id)])

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username    

# Demo Table
class ContectUs(models.Model):
    name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=150)
    message = models.CharField(max_length=255)  # Note: In a real-world scenario, you'd use a more secure way to store passwords

    def __str__(self):
        return self.name

class Info(models.Model):
    name = models.CharField(max_length=150, unique=True)
    city = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name


