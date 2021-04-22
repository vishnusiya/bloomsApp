import string
import random
import os,csv
import string 
import requests
import json, base64, traceback, sys
from django.core.files import File
import re

from decimal import Decimal
from datetime import datetime

from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound

from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
from django.db import transaction
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

from django.contrib.auth.models import User
from django.db.models import Q
import re
# import pandas 
from django.contrib.auth.models import User
from django.db import transaction
import requests
# from bs4 import BeautifulSoup
from datetime import datetime
from app_shop.models import *

@require_POST
def user_login(request):
    try:
        username = request.POST.get('username')
        if username in [None,'']:
            return HttpResponse(content=json.dumps("username not available"), content_type="application/json", status=406)
        
        password = request.POST.get('password')
        if password in [None,'']:
            return HttpResponse(content=json.dumps("password not available"), content_type="application/json", status=406)

        user = User.objects.filter(is_active=True,username=username)
        if not user.exists():
            return HttpResponse(content=json.dumps("Invalid username or password"), content_type="application/json", status=406)
        user = user[0]

        login(request, user)
        return HttpResponse(content=json.dumps("Successfully"), status=200, content_type="application/json")
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        return HttpResponse(content=json.dumps("Invalid username or password"), content_type="application/json", status=406)


##function for getting products category lists
@require_GET
@login_required
def product_category_list_get(request):
    try:
        user = request.user
        categories = ProductCategory.objects.filter(is_active=True).order_by('id')

        search_term = request.GET.get('search_term')
        if search_term not in [None, '']:
            categories = categories.filter(category_name__icontains=search_term)
        
        categories_lst = []
        with transaction.atomic():
            for category in categories:
                category_dict = {}
                category_dict['category_id'] = category.id
                category_dict['category_name'] = category.category_name
                categories_lst.append(category_dict)

            result_dict = {}
            result_dict['categories_lst'] = categories_lst
            return HttpResponse(content=json.dumps(categories_lst), status=200, content_type="application/json")
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        return HttpResponse(content=json.dumps(err), status=406, content_type="application/json")



@require_POST
def create_product(request):
    try:
        user = request.user
        category_name = request.POST.get('category_name')
        product_name = request.POST.get('product_name')
        s_price = request.POST.get('s_price')
        stock_status = request.POST.get('stock_status')
        quantity = request.POST.get('quantity')

        if product_name in [None,'']:
            return HttpResponse(content=json.dumps("Please enter product name"), content_type="application/json", status=406)

        if s_price in [None,'']:
            s_price = 0
            # return HttpResponse(content=json.dumps("Please enter product price"), content_type="application/json", status=406)

        if stock_status in [None,'']:
            return HttpResponse(content=json.dumps("Please select stock status"), content_type="application/json", status=406)

        if quantity in [None,'']:
            return HttpResponse(content=json.dumps("Please enter product quantity"), content_type="application/json", status=406)

        if category_name in [None,'']:
            return HttpResponse(content=json.dumps("Please enter product category"), content_type="application/json", status=406)
        
        with transaction.atomic():
            old_category_obj = ProductCategory.objects.filter(is_active=True,category_name=category_name)
            if old_category_obj.exists():
                category_obj = old_category_obj[0]

            else:
                category_obj = ProductCategory(
                    category_name = category_name,
                    created_by = user,
                    modified_by = user,
                    )
                category_obj.full_clean()
                category_obj.save()

            
            old_product_obj = Product.objects.filter(is_active=True,product_name=product_name,productcategory=category_obj)
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
                    created_by = user,
                    modified_by = user,
                    )
                product_obj.full_clean()
                product_obj.save()
            return HttpResponse(content=json.dumps("Product created Successfully"), status=200, content_type="application/json")
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        return HttpResponse(content=json.dumps(err), content_type="application/json", status=406)



@require_POST
def update_product(request):
    try:
        user = request.user
        user = User.objects.get(is_active=True,id=user.id)
        product_id = request.POST.get('product_id')
        category_name = request.POST.get('category_name')
        product_name = request.POST.get('product_name')
        s_price = request.POST.get('s_price')
        stock_status = request.POST.get('stock_status')
        quantity = request.POST.get('quantity')


        if product_name in [None,'']:
            return HttpResponse(content=json.dumps("Please enter product name"), content_type="application/json", status=406)

        if s_price in [None,'']:
            s_price = 0
            # return HttpResponse(content=json.dumps("Please enter product price"), content_type="application/json", status=406)

        if stock_status in [None,'']:
            return HttpResponse(content=json.dumps("Please select stock status"), content_type="application/json", status=406)

        if quantity in [None,'']:
            return HttpResponse(content=json.dumps("Please enter product quantity"), content_type="application/json", status=406)

        # if category_name in [None,'']:
        #     return HttpResponse(content=json.dumps("Please enter product category"), content_type="application/json", status=406)

        with transaction.atomic():
            Product.objects.filter(is_active=True,id=product_id).update(product_name=product_name,s_price=s_price,stock_status=stock_status,quantity=quantity,modified_by=user)
            return HttpResponse(content=json.dumps("Product Updated Successfully"), status=200, content_type="application/json")
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        return HttpResponse(content=json.dumps(err), content_type="application/json", status=406)


@require_POST
def update_product_quantity(request):
    try:
        user = request.user
        user = User.objects.get(is_active=True,id=user.id)
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        click_type = request.POST.get('click_type')

        if click_type in [None,'']:
            return HttpResponse(content=json.dumps("Please click properly"), content_type="application/json", status=406)

        with transaction.atomic():
            if click_type == 'Increment':                
                quantity = int(quantity) + 1
            else:
                quantity = int(quantity) - 1
            Product.objects.filter(is_active=True,id=product_id).update(quantity=quantity,modified_by=user)
            return HttpResponse(content=json.dumps("Product Updated Successfully"), status=200, content_type="application/json")
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        return HttpResponse(content=json.dumps(err), content_type="application/json", status=406)


@require_POST
def delete_product(request):
    try:
        user = request.user
        user = User.objects.get(is_active=True,id=user.id)
        product_id = request.POST.get('product_id')
        with transaction.atomic():
            product = Product.objects.get(is_active=True,id=product_id)
            product.is_active = False
            product.full_clean()
            product.save()
            return HttpResponse(content=json.dumps("Product Deleted Successfully"), status=200, content_type="application/json")
    except Product.DoesNotExist:
        return HttpResponse(content=json.dumps('Product does not exist'), status=406, content_type="application/json")
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        return HttpResponse(content=json.dumps(err), content_type="application/json", status=406)


##function for getting products lists
@require_GET
@login_required
def product_list_get(request):
    try:
        user = request.user
        category_id = request.GET.get('category_id')
        products = Product.objects.filter(is_active=True,productcategory=category_id).order_by('id')

        search_term = request.GET.get('search_term')
        if search_term not in [None, '']:
            products = products.filter(Q(stock_status__icontains=search_term)|Q(product_name__icontains=search_term))
        
        product_lst = []

        count = products.count()
        page_number = request.GET.get('page_number')
        if page_number == '' or page_number is None:
            page_number = 1
        else:
            page_number = int(page_number)

        entries_per_page = 10
        page_count = int((count/float(entries_per_page)) + 0.95)
        if page_number * entries_per_page >= count:
            entry_max = count
        else:
            entry_max = page_number * entries_per_page
        if entry_max < 0:
            entry_max = 0
        if (page_number - 1) * entries_per_page < 0:
            entry_min = 0
        else:
            entry_min = (page_number-1) * entries_per_page
        products = products[entry_min:entry_max]  
        

        with transaction.atomic():
            for product in products:
                if product.quantity <= 0:
                    Product.objects.filter(is_active=True,id=product.id).update(stock_status='OUT OF STOCK')
                else:
                    Product.objects.filter(is_active=True,id=product.id).update(stock_status='AVAILABLE')

                product_dict = {}
                product_dict['category_id'] = product.productcategory.id
                product_dict['category_name'] = product.productcategory.category_name
                product_dict['product_id'] = product.id
                product_dict['product_name'] = product.product_name
                # product_dict['p_price'] = str(("%.2f" % product.p_price))
                product_dict['s_price'] = str(("%.2f" % product.s_price))
                product_dict['stock_status'] = product.stock_status
                product_dict['quantity'] = str(("%.0f" % product.quantity))
                # product_dict['minimum_status'] = product.minimum_status
                product_lst.append(product_dict)

            result_dict = {}
            result_dict['page_count'] = page_count
            result_dict['product_lst'] = product_lst
            return HttpResponse(content=json.dumps(result_dict), status=200, content_type="application/json")
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        return HttpResponse(content=json.dumps(err), status=406, content_type="application/json")



##function for getting products details
@require_GET
@login_required
def product_details_get(request):
    try:
        user = request.user
        product_id = request.GET.get('product_id')
        product = Product.objects.get(is_active=True,id=product_id)
        product_dict = {}
        product_dict['category_name'] = product.productcategory.category_name
        product_dict['product_id'] = product.id
        product_dict['product_name'] = product.product_name
        product_dict['s_price'] = str(("%.2f" % product.s_price))
        product_dict['stock_status'] = product.stock_status
        product_dict['quantity'] = str(("%.2f" % product.quantity))
        return HttpResponse(content=json.dumps(product_dict), status=200, content_type="application/json")
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        return HttpResponse(content=json.dumps(err), status=406, content_type="application/json")



##function for getting products lists
@require_GET
@login_required
def get_all_products_list(request):
    try:
        user = request.user
        products = Product.objects.filter(is_active=True).order_by('id')
        product_lst = []    
        with transaction.atomic():
            for product in products:
                if product.quantity > 0:
                    Product.objects.filter(is_active=True,id=product.id).update(stock_status='OUT OF STOCK')
                else:
                    Product.objects.filter(is_active=True,id=product.id).update(stock_status='AVAILABLE')

                product_dict = {}
                product_dict['product_id'] = product.id
                product_dict['product_name'] = product.product_name
                # product_dict['p_price'] = str(("%.2f" % product.p_price))
                product_dict['s_price'] = str(("%.2f" % product.s_price))
                product_dict['stock_status'] = product.stock_status
                product_dict['stock'] = str(("%.2f" % product.quantity))
                product_dict['product_name_s_price'] = product.product_name+"-"+str(("%.0f" % product.s_price))
                product_lst.append(product_dict)
            print('product_lst',product_lst)
            return HttpResponse(content=json.dumps(product_lst), status=200, content_type="application/json")
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        return HttpResponse(content=json.dumps(err), status=406, content_type="application/json")




# customer_purchase sales
@require_POST
def create_customer_sales(request):
    try:
        user = request.user
        sales_date = request.POST.get('sales_date')
        total_amount = request.POST.get('grand_total')
        selected_customer_no = request.POST.get('selected_customer_no')
        customer_name = request.POST.get('selected_customer_name')
        main_products_list = request.POST.get('main_products_list')
        received_amount = request.POST.get('received_amount')
        main_products_list = json.loads(main_products_list)

        if total_amount in [None,'','undefined','null']:
            return HttpResponse(content=json.dumps("Please enter total amount"), content_type="application/json", status=406)

        if main_products_list in [None,'','undefined','null',[]]:
            return HttpResponse(content=json.dumps("Please add atleast one product"), content_type="application/json", status=406)

        if received_amount in [None,'','undefined','null']:
            return HttpResponse(content=json.dumps("Please enter amount"), content_type="application/json", status=406)

        if sales_date not in [None,'','undefined','null']:
            sales_date = datetime.strptime(sales_date, "%Y-%m-%d")

        if customer_name in [None,'','undefined','null']:
            customer_name = None
            # return HttpResponse(content=json.dumps("customer_name not available"), content_type="application/json", status=406)

        if selected_customer_no in [None,'','undefined','null']:
            selected_customer_no = None
            # return HttpResponse(content=json.dumps("selected_customer_no not available"), content_type="application/json", status=406)

        with transaction.atomic():               
            for item in main_products_list:
                product_obj = Product.objects.get(is_active=True,id=item['selected_product_id'])
                if selected_customer_no not in [None,'','undefined','null']:
                    customer_obj = Customer.objects.filter(is_active=True,phone_no=selected_customer_no)
                    if customer_obj.exists():
                        customer_obj = customer_obj[0]
                        customer_obj.total_amount = total_amount
                        customer_obj.customer_name = customer_name
                    else:
                        customer_obj = Customer(
                            product=product_obj,
                            customer_name = customer_name,
                            total_amount = total_amount,
                            phone_no = selected_customer_no,
                            created_by = user,
                            modified_by = user,
                            )
                    customer_obj.full_clean()
                    customer_obj.save()


                old_quantity = product_obj.quantity
                current_value = old_quantity - Decimal(item['selected_quantity'])

                if Decimal(item['selected_quantity']) > product_obj.quantity:
                    return HttpResponse(content=json.dumps(product_obj.product_name +" has Only "+ str(("%.0f" % product_obj.quantity)) + " Stock is Available"), content_type="application/json", status=406)

                if old_quantity < current_value:
                    return HttpResponse(content=json.dumps("out of stoke"), content_type="application/json", status=406)

                product_obj.quantity = old_quantity - Decimal(item['selected_quantity'])
                product_obj.full_clean()
                product_obj.save()

                if product_obj.quantity < 0:
                    Product.objects.filter(is_active=True,id=item['selected_product_id']).update(stock_status='AVAILABLE')
                else:
                    Product.objects.filter(is_active=True,id=item['selected_product_id']).update(stock_status='OUT OF STOCK')

                if sales_date in [None,'','undefined']:
                    sales_date = datetime.now()
                
                sales_obj = Sales(
                    sale_date = sales_date,
                    customer_name = customer_name,
                    product_name = product_obj.product_name,
                    quantity = item['selected_quantity'],
                    sale_price = item['total_price'],
                    total_amount = total_amount,
                    created_by = user,
                    modified_by = user,
                    )
                sales_obj.full_clean()
                sales_obj.save()
            return HttpResponse(content=json.dumps("Purchase created Successfully"), status=200, content_type="application/json")
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        return HttpResponse(content=json.dumps(err), content_type="application/json", status=406)



##function for getting Customer sales list
@require_GET
@login_required
def customer_sales_list_get(request):
    try:
        user = request.user
        sales = Sales.objects.filter(is_active=True).order_by('id')
        date_sort_order = request.GET.get('date_sort_order')
        search_term = request.GET.get('search_term')
        if search_term not in [None, '']:
            sales = sales.filter(Q(customer_name__icontains=search_term)|Q(product_name__icontains=search_term))
        sale_lst = []
        sales = sales.order_by('id')  
        
        count = sales.count()
        page_number = request.GET.get('page_number')
        if page_number == '' or page_number is None:
            page_number = 1
        else:
            page_number = int(page_number)

        entries_per_page = 10
        page_count = int((count/float(entries_per_page)) + 0.95)
        if page_number * entries_per_page >= count:
            entry_max = count
        else:
            entry_max = page_number * entries_per_page
        if entry_max < 0:
            entry_max = 0
        if (page_number - 1) * entries_per_page < 0:
            entry_min = 0
        else:
            entry_min = (page_number-1) * entries_per_page
        sales = sales[entry_min:entry_max]   

        for sale in sales:
            sale_dict = {}
            sale_dict['sale_id'] = sale.id
            sale_dict['sale_date'] = datetime.strftime(sale.sale_date,'%d %b %Y') if sale.sale_date not in [None,''] else ''
            sale_dict['product_name'] = sale.product_name
            sale_dict['customer_name'] = sale.customer_name
            sale_dict['quantity'] = str(("%.0f" % sale.quantity)) 
            sale_dict['sale_price'] = str(("%.2f" % sale.sale_price)) 
            sale_lst.append(sale_dict)

        if date_sort_order not in ['',None,[],'undefined']:
            if date_sort_order=='ascending':
                sale_lst = sorted(sale_lst, key=lambda k: k['sale_date'],reverse=True)
            else:
                sale_lst = sorted(sale_lst, key=lambda k: k['sale_date'],reverse=False)

        result_dict = {}
        result_dict['page_count'] = page_count
        result_dict['sale_lst'] = sale_lst
        return HttpResponse(content=json.dumps(result_dict), status=200, content_type="application/json")
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        return HttpResponse(content=json.dumps(err), status=406, content_type="application/json")


##function for getting Customer lists
@require_GET
@login_required
def customer_list_get(request):
    try:
        user = request.user
        customers = Customer.objects.filter(is_active=True).order_by('id')

        search_term = request.GET.get('search_term')
        if search_term not in [None, '']:
            customers = customers.filter(Q(customer_name__icontains=search_term)|Q(phone_no__icontains=search_term))
            
        customer_lst = []

        count = customers.count()
        page_number = request.GET.get('page_number')
        if page_number == '' or page_number is None:
            page_number = 1
        else:
            page_number = int(page_number)

        entries_per_page = 10
        page_count = int((count/float(entries_per_page)) + 0.95)
        if page_number * entries_per_page >= count:
            entry_max = count
        else:
            entry_max = page_number * entries_per_page
        if entry_max < 0:
            entry_max = 0
        if (page_number - 1) * entries_per_page < 0:
            entry_min = 0
        else:
            entry_min = (page_number-1) * entries_per_page
        customers = customers[entry_min:entry_max]  

        for customer in customers:
            customer_dict = {}
            customer_dict['customer_id'] = customer.id
            customer_dict['customer_name'] = customer.customer_name
            customer_dict['recieved_amount'] = str(("%.2f" % customer.recieved_amount)) if customer.recieved_amount not in [None,''] else ''
            customer_dict['pending_amount'] = str(("%.2f" % customer.pending_amount)) if customer.pending_amount not in [None,''] else ''
            customer_dict['total_amount'] = str(("%.2f" % customer.total_amount)) if customer.total_amount not in [None,''] else ''
            customer_dict['phone_no'] = customer.phone_no
            customer_dict['modified_date'] = datetime.strftime(customer.modified_date,'%d %b %Y') if customer.modified_date not in [None,''] else ''
            customer_lst.append(customer_dict)

        result_dict = {}
        result_dict['page_count'] = page_count
        result_dict['customer_lst'] = customer_lst
        return HttpResponse(content=json.dumps(result_dict), status=200, content_type="application/json")
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        return HttpResponse(content=json.dumps(err), status=406, content_type="application/json")

##function for export producs lists
@require_GET
@login_required
def export_products_list(request):
    try:
        filename = "Product_List.csv"
        if os.path.exists(filename):
            os.remove(filename)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=" + filename
        writer = csv.writer(response)
        writer.writerow(
            [
                "Sl/No",
                "Category",
                "Product",
                "Selling Price",
                "Quantity",  
                "Status"
                "Created Date",         
            ]
        )
        products =  Product.objects.filter(is_active=True).order_by('id')
        sl_no = 0
        for product in products:
            created_date = datetime.strftime(product.created_date,'%d %b %Y %I:%M %p')
            sl_no += 1
            writer.writerow(
                [
                    sl_no,
                    product.productcategory.category_name,
                    product.product_name,
                    str(("%.2f" % product.s_price)),
                    str(("%.0f" % product.quantity)),
                    product.stock_status,
                    created_date,
                ]
            )
        return response        
    except ValidationError as e:
        msg = dict(e)
        msg = list(msg.values())[0][0]
        raise ValidationError(msg)
    except Exception:
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        raise ValidationError(err)


##function for getting Customer lists
@require_GET
@login_required
def get_all_customers_list(request):
    try:
        user = request.user
        customers = Customer.objects.filter(is_active=True).order_by('id')
        customer_lst = []
        for customer in customers:
            customer_dict = {}
            customer_dict['customer_id'] = customer.id
            customer_dict['customer_name'] = customer.customer_name
            customer_dict['recieved_amount'] = str(("%.2f" % customer.recieved_amount)) if customer.recieved_amount not in [None,''] else ''
            customer_dict['pending_amount'] = str(("%.2f" % customer.pending_amount)) if customer.pending_amount not in [None,''] else ''
            customer_dict['phone_no'] = customer.phone_no
            customer_lst.append(customer_dict)
        return HttpResponse(content=json.dumps(customer_lst), status=200, content_type="application/json")
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        return HttpResponse(content=json.dumps(err), status=406, content_type="application/json")



# ## create customer
# @require_POST
# def create_customer(request):
#     try:
#         user = request.user
#         customer_name = request.POST.get('customer_name')
#         phone_no = request.POST.get('phone_no')

#         if customer_name in [None,'']:
#             return HttpResponse(content=json.dumps("customer_name not available"), content_type="application/json", status=406)

#         if phone_no in [None,'']:
#             return HttpResponse(content=json.dumps("phone_no not available"), content_type="application/json", status=406)

#         with transaction.atomic():
#             customer_obj = Customer(
#                 customer_name = customer_name,
#                 recieved_amount = 0,
#                 pending_amount = 0,
#                 total_amount = 0,
#                 phone_no = phone_no,
#                 created_by = user,
#                 modified_by = user,
#                 )
#             customer_obj.full_clean()
#             customer_obj.save()
#             return HttpResponse(content=json.dumps("customer created Successfully"), status=200, content_type="application/json")
#     except Exception as e:
#         exc_type, exc_value, exc_traceback = sys.exc_info()
#         err = "\n".join(traceback.format_exception(*sys.exc_info()))
#         print(err)
#         return HttpResponse(content=json.dumps(err), content_type="application/json", status=406)



# @require_POST
# def create_purchase(request):
#     try:
#         user = request.user
#         purchase_date = request.POST.get('purchase_date')
#         product_id = request.POST.get('product_id')
#         quantity = request.POST.get('quantity')
#         purchase_price = request.POST.get('purchase_price')
#         sales_price = request.POST.get('sales_price')


#         if purchase_price in [None,'','undefined','null']:
#             return HttpResponse(content=json.dumps("purchase_price not available"), content_type="application/json", status=406)

#         if product_id in [None,'','undefined','null']:
#             return HttpResponse(content=json.dumps("product_id not available"), content_type="application/json", status=406)

#         if quantity in [None,'','undefined','null']:
#             return HttpResponse(content=json.dumps("quantity not available"), content_type="application/json", status=406)

#         if sales_price in [None,'','undefined','null']:
#             return HttpResponse(content=json.dumps("sales_price not available"), content_type="application/json", status=406)

#         if purchase_date not in [None,'','undefined','null']:
#             purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
#         with transaction.atomic():
#             product = Product.objects.get(is_active=True,id=product_id)
#             product.p_price = purchase_price
#             product.s_price = sales_price
#             old_quantity = product.stock 
#             product.stock = old_quantity + int(quantity)
#             product.full_clean()
#             product.save()

#             if product.stock <= product.minimum_status:
#                 Product.objects.filter(is_active=True,id=product.id).update(stock_status='OUT OF STOCK')
#             else:
#                 Product.objects.filter(is_active=True,id=product.id).update(stock_status='AVAILABLE')

#             purchase_obj = Purchase(
#                 purchase_date = purchase_date,
#                 product_name = product.product_name,
#                 quantity = quantity,
#                 purchase_price = purchase_price,
#                 sales_price = sales_price,
#                 created_by = user,
#                 modified_by = user,
#                 )
#             purchase_obj.full_clean()
#             purchase_obj.save()
#             return HttpResponse(content=json.dumps("Purchase created Successfully"), status=200, content_type="application/json")
#     except Exception as e:
#         exc_type, exc_value, exc_traceback = sys.exc_info()
#         err = "\n".join(traceback.format_exception(*sys.exc_info()))
#         print(err)
#         return HttpResponse(content=json.dumps(err), content_type="application/json", status=406)



# ##function for getting Customer lists
# @require_GET
# @login_required
# def purchase_list_get(request):
#     try:
#         user = request.user
#         purchases = Purchase.objects.filter(is_active=True).order_by('id')
#         date_sort_order = request.GET.get('date_sort_order')
#         search_term = request.GET.get('search_term')
#         if search_term not in [None, '']:
#             purchases = purchases.filter(product_name__icontains=search_term)
            
#         purchase_lst = []
#         count = purchases.count()
#         page_number = request.GET.get('page_number')
#         if page_number == '' or page_number is None:
#             page_number = 1
#         else:
#             page_number = int(page_number)

#         entries_per_page = 10
#         page_count = int((count/float(entries_per_page)) + 0.95)
#         if page_number * entries_per_page >= count:
#             entry_max = count
#         else:
#             entry_max = page_number * entries_per_page
#         if entry_max < 0:
#             entry_max = 0
#         if (page_number - 1) * entries_per_page < 0:
#             entry_min = 0
#         else:
#             entry_min = (page_number-1) * entries_per_page
#         purchases = purchases[entry_min:entry_max]

#         for purchase in purchases:
#             purchase_dict = {}
#             purchase_dict['purchase_id'] = purchase.id
#             purchase_dict['purchase_date'] = datetime.strftime(purchase.purchase_date,'%d %b %Y') if purchase.purchase_date not in [None,''] else ''
#             purchase_dict['product_name'] = purchase.product_name
#             purchase_dict['quantity'] = str(("%.2f" % purchase.quantity)) 
#             purchase_dict['purchase_price'] = str(("%.2f" % purchase.purchase_price)) 
#             purchase_dict['sales_price'] = str(("%.2f" % purchase.sales_price)) 
#             purchase_lst.append(purchase_dict)

#         if date_sort_order not in ['',None,[],'undefined']:
#             if date_sort_order=='ascending':
#                 purchase_lst = sorted(purchase_lst, key=lambda k: k['purchase_date'],reverse=True)
#             else:
#                 purchase_lst = sorted(purchase_lst, key=lambda k: k['purchase_date'],reverse=False)

#         result_dict = {}
#         result_dict['page_count'] = page_count
#         result_dict['purchase_lst'] = purchase_lst
#         return HttpResponse(content=json.dumps(result_dict), status=200, content_type="application/json")
#     except Exception as e:
#         exc_type, exc_value, exc_traceback = sys.exc_info()
#         err = "\n".join(traceback.format_exception(*sys.exc_info()))
#         print(err)
#         return HttpResponse(content=json.dumps(err), status=406, content_type="application/json")


