from django.db import models
from django.contrib.auth.models import User


## Table for saving Sales details.
class Sales(models.Model):
    sale_date = models.DateTimeField(blank=True, null=True)
    customer_name = models.CharField(max_length=900,blank=True, null=True)
    product_name = models.CharField(max_length=900,blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='+')
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='+')
