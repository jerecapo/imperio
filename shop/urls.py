"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

urlpatterns = [
    url(r'^obtenerProductosJson/', 'shop.views.obtenerProductosJson', name='obtenerProductosJson'),

    url(r'^emptyCart/', 'shop.views.emptyCart', name='emptyCart'),
    url(r'^addProductCart/', 'shop.views.addProductCart', name='addProductCart'),
    url(r'^lessProductCart/', 'shop.views.lessProductCart', name='lessProductCart'),
    
    url(r'^shop/', 'shop.views.shop', name='shop'),
    url(r'^producto/', 'shop.views.producto', name='producto'),
    url(r'^$', 'shop.views.index', name='index'),
]