from django.conf.urls import url
from django.conf.urls import url
from app_frontend.views import admin_site

urlpatterns = [
  url(r'^$', admin_site.login_user),
  url(r'^login/$', admin_site.login_user),
  url(r'^home/$', admin_site.home),
  url(r'^logout/$', admin_site.logout_user),

  url(r'^product/create/$', admin_site.product_create),
  url(r'^product/details/(?P<id>\d+)$', admin_site.product_details),
  url(r'^product/list/(?P<id>\d+)$', admin_site.product_list),

  url(r'^customer/create/$', admin_site.customer_create),
  url(r'^customer/list/$', admin_site.customer_list),
  
  url(r'^purchase/create/$', admin_site.purchase_create),
  url(r'^purchase/list/$', admin_site.purchase_list),

  url(r'^customer/sales/create/$', admin_site.customer_sales_create),
  url(r'^customer/sales/list/$', admin_site.customer_sales_list),
]

