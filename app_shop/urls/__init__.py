from django.conf.urls import url, include

urlpatterns = [
    url("", include("app_shop.urls.shop_management")),
]
