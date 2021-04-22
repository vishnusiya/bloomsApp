from django.db import models
from django.contrib.auth.models import User
from ..models import ProductCategory


## Table for saving Product details.
class Product(models.Model):
    productcategory = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=900,blank=True, null=True)
    s_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_status = models.CharField(max_length=900,blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='+')
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='+')
    # p_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    # minimum_status = models.IntegerField(blank=True, null=True)

