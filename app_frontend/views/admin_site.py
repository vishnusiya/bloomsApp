import string   #Vishnupriya
import random    #Vishnupriya
import sys   #Vishnupriya
import traceback    #Vishnupriya
import json  #Vishnupriya
import os   #Vishnupriya
import requests #Vishnupriya
from django.conf import settings#Vishnupriya

from django.shortcuts import render, redirect
from datetime import timedelta #Vishnupriya
import datetime as dt
from datetime import datetime, time #Vishnupriya
from django.db.models import Q   #Vishnupriya
from django.http import HttpResponse  #Vishnupriya
from django.contrib.auth.decorators import login_required  #Vishnupriya
from django.views.decorators.http import require_GET     #Vishnupriya
from django.views.decorators.http import require_POST    #Vishnupriya
from django import db   #Vishnupriya
from django.db import transaction  #Vishnupriya
from django.contrib.auth.models import User  #Vishnupriya
from django.core.exceptions import ValidationError #Vishnupriya
from django.core.files import File #Vishnupriya
from django.core.mail import EmailMessage #Vishnupriya
from django.db.models import Sum #Vishnupriya
from app_shop.models import *  #Vishnupriya
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.contrib.auth import authenticate, login, logout



def login_user(request):
    return render(request, 'admin/login.html')

def home(request):
    return render(request, 'admin/home.html')

@login_required
def logout_user(request):
    logged_user = request.user
    logout(request)    
    return HttpResponseRedirect('/')


@login_required
def product_create(request):
    return render(request, 'admin/product_create.html')


@login_required
def product_details(request,id):
    return render(request, 'admin/product_details.html')


@login_required
def product_list(request,id):
    return render(request, 'admin/product_list.html')



@login_required
def customer_create(request):
    return render(request, 'admin/customer_create.html')


@login_required
def customer_list(request):
    return render(request, 'admin/customer_list.html')


@login_required
def purchase_create(request):
    return render(request, 'admin/purchase_create.html')


@login_required
def purchase_list(request):
    return render(request, 'admin/purchase_list.html')



@login_required
def customer_sales_create(request):
    return render(request, 'admin/customer_sales_create.html')


@login_required
def customer_sales_list(request):
    return render(request, 'admin/customer_sales_list.html')