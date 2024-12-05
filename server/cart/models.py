from django.db import models
from products.models import *

# Create your models here.
class CartItemsModel(models.Model):
    STATUS_CHOICES = [
        ('InCart', 'In Cart'),
        ('Order', 'Order'),
        ('Purchased', 'Purchased'),
        ('Complete', 'Complete'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    
    reference = models.CharField(max_length=500, null=True, blank=True)
    current_user = models.CharField(max_length=1000, null=True, blank=True)
    product = models.ForeignKey(ProductModel, null=True, on_delete=models.CASCADE,
                              blank=True, default=None, related_name='product')
    quantity = models.IntegerField(null=True,blank=True) 
    total = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=1000, null=True, blank=True, default='InCart', choices=STATUS_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.current_user
    
class CustomerOrderModel(models.Model):
    ORDER_CHOICES = [
        ('Order', 'Order'),
        ('Purchased', 'Purchased'),
        ('Pending', 'Pending'),
        ('returned', 'returned'),
        ('Complete', 'Complete'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    reference = models.CharField(max_length=500, null=True, blank=True)
    current_user = models.CharField(max_length=1000, null=True, blank=True)
    full_name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    phone_number = models.CharField(max_length=50,null=True)
    street = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    province = models.CharField(max_length=200,null=True)
    postal_code = models.CharField(max_length=200,null=True)
    customer_items = models.ManyToManyField(
        CartItemsModel, blank=True, default=None, related_name='customer_items')
    total = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=1000, null=True, blank=True, default='Oder', choices=ORDER_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.full_name