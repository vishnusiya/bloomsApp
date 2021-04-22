from django.db import models
from django.contrib.auth.models import User
from .product import Product



## Table for saving Customer details.
class Customer(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=900,blank=True, null=True)
    # customer_number = models.CharField(max_length=900,blank=True, null=True)
    recieved_amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    pending_amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    phone_no = models.FloatField(max_length=900,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='+')
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='+')