from django.conf.urls import url
from app_shop.views import shop_management


urlpatterns = [
    url(r'^user/login/$', shop_management.user_login),
    url(r'^product/category/list/get$', shop_management.product_category_list_get),
    url(r'^product/list/get$', shop_management.product_list_get),

    url(r'^product/create/$', shop_management.create_product),
    url(r'^product/update/$', shop_management.update_product),
    url(r'^product/delete/$', shop_management.delete_product),
    url(r'^product/details/get$', shop_management.product_details_get),
    url(r'^update/product/quantity/$', shop_management.update_product_quantity),
    url(r'^export/products/csv/$', shop_management.export_products_list),

    url(r'^customer/list/get$', shop_management.customer_list_get),   
    # url(r'^customer/create/$', shop_management.create_customer),
    # url(r'^purchase/create/$', shop_management.create_purchase),
    # url(r'^purchase/list/get$', shop_management.purchase_list_get),


    url(r'^customer/purchase/sales$', shop_management.create_customer_sales),
    url(r'^customer/sales/list/get$', shop_management.customer_sales_list_get),
    
    url(r'^get/all/products/list$', shop_management.get_all_products_list),
    url(r'^get/all/customers/list$', shop_management.get_all_customers_list),
    ]