import os #Vishnupriya
import os.path #Vishnupriya
import json #Vishnupriya
import sys,string,random,csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_shop.settings') #Vishnupriya

import django #Vishnupriya
django.setup() #Vishnupriya


from django.contrib.auth.models import User
from django.db import transaction
from app_shop.models import *
from decimal import Decimal


if __name__ == '__main__':
    print ('Starting database population...')
    users = open('1.Blooms_Stock_28-Apr-2021.csv')
    users = open('1.Blooms_Stock_28-Apr-2021.csv')
    count = 0
    admin = User.objects.get(is_active=True,username='admin')
    with transaction.atomic():
        for row in users:
            row = row.split(',')
            print(11111111111,row)
            category_name = row[1]
            product_name = row[2]
            quantity = row[4]
            s_price = row[3]
            with transaction.atomic():
                if category_name not in [None,'',""]:
                    old_category_obj = ProductCategory.objects.filter(is_active=True,category_name=category_name)
                    if old_category_obj.exists():
                        category_obj = old_category_obj[0]
                    else:
                        category_obj = ProductCategory(
                            category_name = category_name,
                            created_by = admin,
                            modified_by = admin,
                            )
                        category_obj.full_clean()
                        category_obj.save()

                    old_product_obj = Product.objects.filter(is_active=True,product_name=product_name,productcategory=category_obj,s_price=s_price)
                    if old_product_obj.exists():
                        old_product_obj = old_product_obj[0]
                        old_product_obj.quantity += Decimal(quantity)
                        old_product_obj.s_price = s_price
                        old_product_obj.save()
                    else:
                        product_obj = Product(
                            productcategory=category_obj,
                            product_name = product_name,
                            s_price = s_price,
                            quantity = quantity,
                            stock_status = 'AVAILABLE',
                            created_by = admin,
                            modified_by = admin,
                            )
                        product_obj.full_clean()
                        product_obj.save()

                    print("Product saved : ",str(count))
                    count += 1            
        print ("Product Created Sucessfully!!!")