"""sistema URL Configuration

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
from django.conf.urls import url, include, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 

urlpatterns = [
    url(r'^dashboard/', 'ventas.views.dashboard', name='dashboard'),
    url(r'^imprimir/', 'ventas.views.imprimir', name='imprimir'),
    url(r'^importar/', 'ventas.views.importar', name='importar'),
    url(r'^normalizar_stock/', 'ventas.views.normalizar_stock', name='normalizar_stock'),
    url(r'^descargar_excel_productos/', 'ventas.views.descargar_excel_productos', name='descargar_excel_productos'),
    url(r'^descargar_excel_clientes/', 'ventas.views.descargar_excel_clientes', name='descargar_excel_clientes'),
    url(r'^descargar_excel_producto_pedido/', 'ventas.views.descargar_excel_producto_pedido', name='descargar_excel_producto_pedido'),
    url(r'^reporte_lista_clientes/', 'ventas.views.reporte_lista_clientes', name='reporte_lista_clientes'),
    url(r'^reporte_lista_productos/', 'ventas.views.reporte_lista_productos', name='reporte_lista_productos'),
    url(r'^reporte_producto_pedido/', 'ventas.views.reporte_producto_pedido', name='reporte_producto_pedido'),
    url(r'^reporte_cantidad_productos/', 'ventas.views.reporte_cantidad_productos', name='reporte_cantidad_productos'),
    url(r'^reporte_cliente_productos/', 'ventas.views.reporte_cliente_productos', name='reporte_cliente_productos'),
    url(r'^reporte_gastos/', 'ventas.views.reporte_gastos', name='reporte_gastos'),
    url(r'^obtener_cliente/', 'ventas.views.obtener_cliente', name='obtener_cliente'),
    url(r'^obtener_producto/', 'ventas.views.obtener_producto', name='obtener_producto'),
    url(r'^shop/', include('shop.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'ventas.views.index', name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

