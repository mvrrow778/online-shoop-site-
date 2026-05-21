from django.db import models

class Category (models.Model):
    name = models.CharField (max_length = 20, verbose_name = "Category name")

    def __str__ (self):
        return self.name

class Product (models.Model):
    category = models.ForeignKey (Category, on_delete=models.CASCADE, verbose_name = "Category")
    name = models.CharField (max_length=30, verbose_name = "Product name")
    price = models.DecimalField (max_digits = 10, decimal_places = 2, verbose_name = "Price")
    description = models.TextField (blank=True, verbose_name="Product description")
    quantity = models.IntegerField (default = 0, verbose_name = "Remaining in stock: ")
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Product photo")

    def __str__ (self):
        return self.name

class Sale(models.Model):
    product = models.ForeignKey (Product, on_delete = models.CASCADE, verbose_name = "Product")
    sale_date = models.DateTimeField (auto_now_add=True, verbose_name = "Date of sale")
    amount = models.IntegerField (default = 1, verbose_name = "Quantity of purchased item")

    def __str__(self):
        return f"Sale: {self.product.name} ({self.sale_date.strftime('%d.%m %H:%M')})"

from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('cashier', 'Cashier'),
        ('stockman', 'Stockmanpython manage.py runserver'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()