#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import loader
from django.template.defaulttags import register
from django.http import HttpResponse
from django.utils.translation import ugettext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Pedido, Producto, Cliente, ProductoPedido, Gasto, Proveedor
from datetime import date, timedelta
import json
import collections
import datetime

def index(request):
    mensaje = ''
    
    context = {'mensaje': mensaje,}
    return render(request, 'web/index.html', context)

@login_required
def dashboard(request):
    mensaje = ''
    
    context = {'mensaje': mensaje }
    return render(request, 'reportes/dashboard.html', context)
    
@login_required
def imprimir(request):
    LIMITE_LINEAS_EXTRAS = 28
    
    pedido_id = request.GET.get('pedido_id', '')
    pedido = Pedido.objects.get(pk=pedido_id)
    
    cantidad_productos = pedido.productopedido_set.all().count()
    prod_extras = LIMITE_LINEAS_EXTRAS - cantidad_productos
    lineas_prod_extras = "x" * prod_extras
    
    total = 0
    for pp in pedido.productopedido_set.all():
        total = total + pp.total
    
    context = {'pedido': pedido, 'lineas_prod_extras': lineas_prod_extras, 'total':total, }
    return render(request, 'reportes/pedido.html', context)

@login_required
def reporte_lista_productos(request):
    productos = Producto.objects.all()

    context = {'productos': productos, }
    return render(request, 'reportes/reporte_lista_productos.html', context)

@login_required
def reporte_lista_clientes(request):
    clientes= Cliente.objects.all()

    context = {'clientes': clientes, }
    return render(request, 'reportes/reporte_lista_clientes.html', context)

@login_required
def reporte_cantidad_productos(request):

    if request.method == 'GET':
        fechaDesde = "2000-01-01"
        fechaHasta = "2050-01-02"
    elif request.method == 'POST':
        fechaDesde = request.POST.get('fechaDesde',"2000-01-01")
        fechaHasta = request.POST.get('fechaHasta',"2050-01-10")

    fecha_fecha_hasta = datetime.datetime.strptime(fechaHasta, '%Y-%m-%d').date()
    d = fecha_fecha_hasta+timedelta(days=1)
    fechaHasta = d.strftime("%Y-%m-%d")

    pp = ProductoPedido.objects.filter(pedido__fecha__range=[fechaDesde, fechaHasta])

    costo = 0
    venta = 0    
    ganancia = 0    
    cant  = 0
    dict  = {}

    for p in pp:
        ganancia = ganancia + (p.total - (p.producto.precio_costo * p.cantidad_productos))
        costo = costo + p.producto.precio_costo * p.cantidad_productos
        venta = venta + p.total
        cant = cant + p.cantidad_productos
        if dict.has_key(p.producto.nombre):
            dict_int = dict.get(p.producto.nombre)
            dict_int['venta'] = dict_int['venta'] + p.total
            dict_int['costo'] = dict_int['costo'] + p.producto.precio_costo * p.cantidad_productos
            dict_int['ganancia'] = dict_int['ganancia'] + (p.total - (p.producto.precio_costo * p.cantidad_productos))
            dict_int['cantidad'] = dict_int['cantidad'] + p.cantidad_productos
            dict[p.producto.nombre] = dict_int
        else:
            dict_int = {}
            dict_int['venta'] = p.total
            dict_int['costo'] = p.producto.precio_costo * p.cantidad_productos
            dict_int['ganancia'] = p.total - (p.producto.precio_costo * p.cantidad_productos)
            dict_int['cantidad'] = p.cantidad_productos
            dict[p.producto.nombre] = dict_int
        
    od = collections.OrderedDict(sorted(dict.items()))

    fecha_fecha_hasta = datetime.datetime.strptime(fechaHasta, '%Y-%m-%d').date()
    d = fecha_fecha_hasta-timedelta(days=1)
    fechaHasta = d.strftime("%Y-%m-%d")

    context = {'dict': od, 'ganancia': ganancia, 'costo':costo, 'venta':venta, 'cant': cant, 'fechaDesde': fechaDesde, 'fechaHasta': fechaHasta }
    return render(request, 'reportes/reporte_cantidad_productos.html', context)

@login_required
def reporte_cliente_productos(request):

    if request.method == 'GET':
        fechaDesde = "2000-01-01"
        fechaHasta = "2050-01-02"
    elif request.method == 'POST':
        fechaDesde = request.POST.get('fechaDesde',"2000-01-01")
        fechaHasta = request.POST.get('fechaHasta',"2050-01-10")

    fecha_fecha_hasta = datetime.datetime.strptime(fechaHasta, '%Y-%m-%d').date()
    d = fecha_fecha_hasta+timedelta(days=1)
    fechaHasta = d.strftime("%Y-%m-%d")

    pp = ProductoPedido.objects.filter(pedido__fecha__range=[fechaDesde, fechaHasta])
    
    costo = 0
    venta = 0    
    ganancia = 0    
    cant  = 0
    dict  = {}

    for p in pp:
        ganancia = ganancia + (p.total - (p.producto.precio_costo * p.cantidad_productos))
        costo = costo + p.producto.precio_costo * p.cantidad_productos
        venta = venta + p.total
        cant = cant + p.cantidad_productos
        if dict.has_key(p.pedido.cliente.cliente):
            dict_int = dict.get(p.pedido.cliente.cliente)
            dict_int['venta'] = dict_int['venta'] + p.total
            dict_int['costo'] = dict_int['costo'] + p.producto.precio_costo * p.cantidad_productos
            dict_int['ganancia'] = dict_int['ganancia'] + (p.total - (p.producto.precio_costo * p.cantidad_productos))
            dict_int['cantidad'] = dict_int['cantidad'] + p.cantidad_productos
            dict[p.pedido.cliente.cliente] = dict_int
        else:
            dict_int = {}
            dict_int['venta'] = p.total
            dict_int['costo'] = p.producto.precio_costo * p.cantidad_productos
            dict_int['ganancia'] = p.total - (p.producto.precio_costo * p.cantidad_productos)
            dict_int['cantidad'] = p.cantidad_productos
            dict[p.pedido.cliente.cliente] = dict_int
        
    od = collections.OrderedDict(sorted(dict.items()))

    fecha_fecha_hasta = datetime.datetime.strptime(fechaHasta, '%Y-%m-%d').date()
    d = fecha_fecha_hasta-timedelta(days=1)
    fechaHasta = d.strftime("%Y-%m-%d")

    context = {'dict': od, 'ganancia': ganancia, 'costo':costo, 'venta':venta, 'cant': cant, 'fechaDesde': fechaDesde, 'fechaHasta': fechaHasta }
    return render(request, 'reportes/reporte_cliente_productos.html', context)

@login_required
def reporte_producto_pedido(request):

    if request.method == 'GET':
        fechaDesde = "2000-01-01"
        fechaHasta = "2050-01-02"
    elif request.method == 'POST':
        fechaDesde = request.POST.get('fechaDesde',"2000-01-01")
        fechaHasta = request.POST.get('fechaHasta',"2050-01-10")

    fecha_fecha_hasta = datetime.datetime.strptime(fechaHasta, '%Y-%m-%d').date()
    d = fecha_fecha_hasta+timedelta(days=1)
    fechaHasta = d.strftime("%Y-%m-%d")
        
    pp = ProductoPedido.objects.filter(pedido__fecha__range=[fechaDesde, fechaHasta])

    lista = []
    dict  = {}
    total = 0
    cant  = 0
    for p in pp:
        total = total + p.total
        cant  = cant + p.cantidad_productos
        dict  = {}
        dict['fecha']           = p.pedido.fecha
        dict['orden_de_venta']  = p.pedido.orden_de_venta
        dict['cliente']         = p.pedido.cliente.cliente
        dict['nombre']          = p.producto.nombre
        dict['precio']          = p.precio_venta_distribuidor
        dict['cantidad']        = p.cantidad_productos
        dict['descuento']       = p.descuento
        dict['total']           = p.total
        lista.append(dict)
        
    fecha_fecha_hasta = datetime.datetime.strptime(fechaHasta, '%Y-%m-%d').date()
    d = fecha_fecha_hasta-timedelta(days=1)
    fechaHasta = d.strftime("%Y-%m-%d")

    context = {'lista': lista , 'total': total, 'cant': cant, 'fechaDesde': fechaDesde, 'fechaHasta': fechaHasta }
    return render(request, 'reportes/reporte_producto_pedido.html', context)

@login_required
def reporte_gastos(request):

    proveedores = Proveedor.objects.all()

    if request.method == 'GET':
        fechaDesde = "2017-01-01"
        fechaHasta = "2017-12-02"
        proveedor  = 0
    elif request.method == 'POST':
        fechaDesde = request.POST.get('fechaDesde',"2017-01-01")
        fechaHasta = request.POST.get('fechaHasta',"2050-12-01")
        proveedor  = request.POST.get('selectProveedor',0)


    fecha_fecha_hasta = datetime.datetime.strptime(fechaHasta, '%Y-%m-%d').date()
    d = fecha_fecha_hasta+timedelta(days=1)
    fechaHasta = d.strftime("%Y-%m-%d")

    if proveedor == '0' or proveedor == 0 or proveedor == 'TODOS':
        gastos = Gasto.objects.filter(fecha__range=[fechaDesde, fechaHasta])
        proveedor = 'TODOS'
    else:
        gastos = Gasto.objects.filter(fecha__range=[fechaDesde, fechaHasta],proveedor_id=proveedor)
        proveedor = Proveedor.objects.get(id=proveedor).proveedor

    total = 0
    for g in gastos:
        total = total + g.total

    fecha_fecha_hasta = datetime.datetime.strptime(fechaHasta, '%Y-%m-%d').date()
    d = fecha_fecha_hasta-timedelta(days=1)
    fechaHasta = d.strftime("%Y-%m-%d")
        
    context = {
                'gastos'     : gastos , 
                'total'      : total, 
                'fechaDesde' : fechaDesde, 
                'fechaHasta' : fechaHasta,
                'proveedores': proveedores,
                'proveedor'  : proveedor,
            }
    return render(request, 'reportes/reporte_gastos.html', context)
    
@login_required
def importar(request):
    
    return HttpResponse("termino")

@login_required
def obtener_cliente(request):

    id_cliente = request.GET.get('id_cliente')
    cliente = Cliente.objects.get(pk=id_cliente)
    dict = {'direccion': cliente.direccion, 'mail': cliente.email, 'telefono':cliente.telefono}
    return HttpResponse(json.dumps(dict), content_type="application/json")

@login_required
def obtener_producto(request):

    id_producto = request.GET.get('id_producto')
    producto = Producto.objects.get(pk=id_producto)
    dict = { 'precio_venta_publico': producto.precio_venta_publico }
    return HttpResponse(json.dumps(dict), content_type="application/json")

@login_required
def descargar_excel_productos(request):
    import StringIO 
    import xlsxwriter 
    response = HttpResponse(content_type='application/vnd.ms-excel') 
    response['Content-Disposition'] = 'attachment; filename=Listado_Productos.xlsx' 
    output = StringIO.StringIO() 
    workbook = xlsxwriter.Workbook(output) 
    worksheet_s = workbook.add_worksheet("Productos") 
    title = workbook.add_format({ 'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter' })
    header = workbook.add_format({ 'bg_color': '#F7F7F7', 'color': 'black', 'align': 'center', 'valign': 'top', 'border': 1 }) 
    title_text = u"{0} {1}".format(ugettext("Listado de Productos Growtech"), "") 
    worksheet_s.merge_range('A2:B2', title_text, title) 
    worksheet_s.write(4, 0, ugettext("Nombre"), header) 
    worksheet_s.write(4, 1, ugettext("Precio"), header) 
    productos = Producto.objects.all() 
    linea = 0 
    description_col_width = 10
    for pp in productos: 
        linea = linea + 1
        row = 5 + linea 
        worksheet_s.write_string(row, 0, pp.nombre)
        worksheet_s.write_number(row, 1, pp.precio_venta_distribuidor) 
        if len(pp.nombre) > description_col_width: 
            description_col_width = len(pp.nombre)
    worksheet_s.set_column('A:A', description_col_width) 
    workbook.close()
    xlsx_data = output.getvalue() 
    response.write(xlsx_data) 
    return response
        
@login_required
def descargar_excel_clientes(request):
    import StringIO 
    import xlsxwriter 
    response = HttpResponse(content_type='application/vnd.ms-excel') 
    response['Content-Disposition'] = 'attachment; filename=Listado_Clientes.xlsx' 
    output = StringIO.StringIO() 
    workbook = xlsxwriter.Workbook(output) 
    worksheet_s = workbook.add_worksheet("Productos") 
    title = workbook.add_format({ 'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter' })
    header = workbook.add_format({ 'bg_color': '#F7F7F7', 'color': 'black', 'align': 'center', 'valign': 'top', 'border': 1 }) 
    title_text = u"{0} {1}".format(ugettext("Listado de Clientes Growtech"), "") 
    worksheet_s.merge_range('A2:B2', title_text, title) 
    worksheet_s.write(4, 0, ugettext("Nombre"), header) 
    worksheet_s.write(4, 1, ugettext("Contacto"), header) 
    worksheet_s.write(4, 2, ugettext("Telefono"), header) 
    worksheet_s.write(4, 3, ugettext("Celular"), header) 
    worksheet_s.write(4, 4, ugettext("Mail"), header) 
    worksheet_s.write(4, 5, ugettext("Direccion"), header) 
    clientes= Cliente.objects.all() 
    linea = 0 
    description_col_width = 10
    for pp in clientes: 
        linea = linea + 1
        row = 5 + linea 
        worksheet_s.write_string(row, 0, pp.cliente)
        worksheet_s.write_string(row, 1, pp.contacto) 
        worksheet_s.write_string(row, 2, pp.telefono) 
        worksheet_s.write_string(row, 3, pp.celular) 
        worksheet_s.write_string(row, 4, pp.email) 
        worksheet_s.write_string(row, 5, pp.direccion) 
        if len(pp.cliente) > description_col_width: 
            description_col_width = len(pp.cliente)
    worksheet_s.set_column('A:A', description_col_width) 
    workbook.close()
    xlsx_data = output.getvalue() 
    response.write(xlsx_data) 
    return response

@login_required
def descargar_excel_producto_pedido(request):
    import StringIO 
    import xlsxwriter 
    response = HttpResponse(content_type='application/vnd.ms-excel') 
    response['Content-Disposition'] = 'attachment; filename=Productos_x_Pedido.xlsx' 
    output = StringIO.StringIO() 
    workbook = xlsxwriter.Workbook(output) 
    worksheet_s = workbook.add_worksheet("Productos_x_Pedido") 
    title = workbook.add_format({ 'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter' })
    header = workbook.add_format({ 'bg_color': '#F7F7F7', 'color': 'black', 'align': 'center', 'valign': 'top', 'border': 1 }) 
    title_text = u"{0} {1}".format(ugettext("Productos por Pedidos"), "") 
    worksheet_s.merge_range('A2:B2', title_text, title) 
    worksheet_s.write(4, 0, ugettext("Fecha"), header) 
    worksheet_s.write(4, 1, ugettext("Orden de venta"), header) 
    worksheet_s.write(4, 2, ugettext("Cliente"), header) 
    worksheet_s.write(4, 3, ugettext("Producto"), header) 
    worksheet_s.write(4, 4, ugettext("Precio"), header) 
    worksheet_s.write(4, 5, ugettext("Cantidad"), header) 
    worksheet_s.write(4, 6, ugettext("Descuento"), header)
    worksheet_s.write(4, 7, ugettext("Total"), header)
    
    fechaDesde = request.GET.get('fechaDesde',"2000-01-01")
    fechaHasta = request.GET.get('fechaHasta',"2050-01-01")

    if fechaDesde == "":
        fechaDesde = "2000-01-01"
    if fechaHasta == "":
        fechaHasta = "2050-01-01"

    fecha_fecha_hasta = datetime.datetime.strptime(fechaHasta, '%Y-%m-%d').date()
    d = fecha_fecha_hasta+timedelta(days=1)
    fechaHasta = d.strftime("%Y-%m-%d")
  
    pp = ProductoPedido.objects.filter(pedido__fecha__range=[fechaDesde, fechaHasta])

    lista = []
    dict  = {}
    total = 0
    cant  = 0
    for p in pp:
        total = total + p.total
        cant  = cant + p.cantidad_productos
        dict  = {}
        dict['fecha']           = p.pedido.fecha.strftime("%d-%m-%Y %H:%M")
        dict['orden_de_venta']  = p.pedido.orden_de_venta
        dict['cliente']         = p.pedido.cliente.cliente
        dict['nombre']          = p.producto.nombre
        dict['precio']          = str(p.precio_venta_distribuidor)
        dict['cantidad']        = str(p.cantidad_productos)
        dict['descuento']       = str(p.descuento)
        dict['total']           = str(p.total)
        lista.append(dict)

    linea = 0 
    description_col_width = 10
    for pp in lista: 
        linea = linea + 1
        row = 5 + linea 
        worksheet_s.write_string(row, 0, pp.get('fecha'))
        worksheet_s.write_string(row, 1, pp.get('orden_de_venta')) 
        worksheet_s.write_string(row, 2, pp.get('cliente')) 
        worksheet_s.write_string(row, 3, pp.get('nombre')) 
        worksheet_s.write_string(row, 4, pp.get('precio')) 
        worksheet_s.write_string(row, 5, pp.get('cantidad')) 
        worksheet_s.write_string(row, 6, pp.get('descuento')) 
        worksheet_s.write_string(row, 7, pp.get('total')) 
        if len(pp.get('nombre')) > description_col_width: 
            description_col_width = len(pp.get('nombre'))
    worksheet_s.set_column('A:A', description_col_width) 
    workbook.close()
    xlsx_data = output.getvalue() 
    response.write(xlsx_data) 
    return response

@login_required
def normalizar_stock(request):
    productos = Producto.objects.all()
    for prod in productos:
        total = 0
        for prod_stock in prod.stock_set.all():
            total = total + prod_stock.actual
        prod.stocks = total
        prod.save()
    return HttpResponse("Listo")

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)