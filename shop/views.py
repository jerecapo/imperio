from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.template.defaulttags import register
from ventas.models import *

import mercadopago
import json


# Create your views here.
def index(request):
    categorias          = Categoria.objects.filter(shop=True).order_by('orden')
    ofertas             = Producto.objects.filter(oferta=True, shop=True)
    destacados          = Producto.objects.filter(destacado=True, shop=True)
    changuito           = get_changuito(request)
    chango              = get_chango(request)
    cantProd, totalProd = get_chango_valores_total(changuito)
    dict_prod  = {}

    context = { 'categorias':categorias,
                'dict_prod':dict_prod,
                'ofertas':ofertas,
                'destacados':destacados,
                'changuito':changuito,
                'chango':chango,
                'cantProd':cantProd,
                'totalProd':totalProd,
            }
    return render(request, 'shop/index.html', context)

# Create your views here.
def shop(request):
    categorias          = Categoria.objects.filter(shop=True).order_by('orden')
    changuito           = get_changuito(request)
    chango              = get_chango(request)
    cantProd, totalProd = get_chango_valores_total(changuito)
    
    cat_select = request.GET.get('categoria_id','0')
    if cat_select == '0':
        productos = Producto.objects.filter(shop=True)
        nombre_cat = 'TODAS'
    else:
        productos = Producto.objects.filter(categoria=cat_select, shop=True)
        nombre_cat = Categoria.objects.get(id=cat_select).nombre

    context = { 'categorias':categorias,
                'productos':productos,
                'changuito':changuito,
                'chango':chango,
                'cantProd':cantProd,
                'totalProd':totalProd,
                'nombreCat':nombre_cat
            }
    return render(request, 'shop/shop.html', context)

def producto(request):
    mensaje             = ''
    prod_id             = request.GET.get('id', '')
    categorias          = Categoria.objects.filter(shop=True).order_by('orden')
    changuito           = get_changuito(request)
    chango              = get_chango(request)
    cantProd, totalProd = get_chango_valores_total(changuito)
    producto            = Producto.objects.get(id=prod_id)

    context = { 'mensaje': mensaje,
                'categorias':categorias,
                'producto':producto,
                'changuito':changuito,
                'chango':chango,
                'cantProd':cantProd,
                'totalProd':totalProd,
            }
    return render(request, 'shop/producto.html', context)

def carretilla(request):
    mensaje             = ''
    categorias          = Categoria.objects.filter(shop=True).order_by('orden')
    changuito           = get_changuito(request)
    chango              = get_chango(request)
    cantProd, totalProd = get_chango_valores_total(changuito)
    adicTarjeta         = (11*totalProd/100)
    totalConTarjeta     = totalProd + adicTarjeta

    urlMP = returnUrlMP(request, changuito)

    context = { 'mensaje': mensaje,
                'categorias':categorias,
                'producto':producto,
                'changuito':changuito,
                'chango':chango,
                'cantProd':cantProd,
                'totalProd':totalProd,
                'adicTarjeta':adicTarjeta,
                'totalConTarjeta':totalConTarjeta,
                'botonMP':urlMP
            }
    return render(request, 'shop/carretilla.html', context)

def regarcaPasoUno(request):
    changuito           = get_changuito(request)
    chango              = get_chango(request)
    cantProd, totalProd = get_chango_valores_total(changuito)
    urlMP = returnUrlMP(request, changuito)

    context = { 
        'changuito':changuito,
        'chango':chango,
        'cantProd':cantProd,
        'totalProd':totalProd,
        'botonMP':urlMP
    }
    return render(request, 'shop/carretilla-paso-uno.html', context)

def addProductCart(request):
    id_prod             = request.POST.get('id_prod_add', '')
    changuito           = get_changuito(request)
    if id_prod in changuito:
        cantidad = changuito.get(id_prod)
        cantidad = cantidad + 1
        changuito[id_prod] = cantidad
    else:
        changuito[id_prod] = 1

    request.session['changuito'] = changuito

    chango              = get_chango(request)
    cantProd, totalProd = get_chango_valores_total(changuito)

    context = { 'chango':chango,
                'cantProd':cantProd,
                'totalProd':totalProd,
                'changuito':changuito,
            }
    return render(request, 'shop/cart.html', context)

def lessProductCart(request):
    id_prod    = request.POST.get('id_prod_less', '')
    changuito                   = get_changuito(request)
    cantidad                    = changuito.get(id_prod)
    cantidad                    = cantidad - 1
    if cantidad == 0:
        del changuito[id_prod]
    else:
        changuito[id_prod]          = cantidad
    request.session['changuito']    = changuito
    chango                      = get_chango(request)
    cantProd, totalProd         = get_chango_valores_total(changuito)

    context = { 'chango':chango,
                'cantProd':cantProd,
                'totalProd':totalProd,
                'changuito':changuito,
            }
    return render(request, 'shop/cart.html', context)

def emptyCart(request):
    request.session['changuito'] = {}
    chango                       = get_chango(request)
    changuito                    = get_changuito(request)
    cantProd, totalProd          = get_chango_valores_total(changuito)
    context = { 'chango':chango,
                'cantProd':cantProd,
                'totalProd':totalProd,
                'changuito':changuito,
            }
    return render(request, 'shop/cart.html', context)

def obtenerProductosJson(request):
    productos = Producto.objects.filter(shop=True)
    data = serializers.serialize('json', productos)
    return HttpResponse(data, content_type='application/json')

def validarNumeroSocio(request):
    response_data = {}
    numeroSocio      = request.POST.get('numeroSocio', '')
    try:
        cliente = Cliente.objects.get(numeroSocio__iexact=numeroSocio)
        print cliente
        response_data['contacto'] = cliente.contacto
        response_data['mail'] = cliente.email
        response_data['telefono'] = cliente.telefono
        response_data['direccion'] = cliente.direccion
        print cliente.direccion
        response_data['error'] = ""
        print response_data
    except Cliente.DoesNotExist:
        response_data['error'] = "No se encontro cliente con ese numero de socio."
        
    return JsonResponse(response_data)


def crearVenta(request):
    changuito   = get_changuito(request)

    urlMP = returnUrlMP(request, changuito)

    numeroSocio = request.POST.get('numeroSocio', '')
    contacto    = request.POST.get('contacto', '')
    mail        = request.POST.get('mail', '')
    telefono    = request.POST.get('telefono', '')
    domicilio   = request.POST.get('domicilio', '')
    comentario  = request.POST.get('comentarios', '')


    if numeroSocio:
        clientes = Cliente.objects.filter(numeroSocio=numeroSocio)
    elif mail:
        clientes = Cliente.objects.filter(email=mail)
    else:
        clientes = None

    if clientes:
        cliente = clientes[0]
    else:
        cliente = Cliente()

    cliente.cliente = contacto
    cliente.contacto = contacto
    cliente.telefono = telefono
    cliente.email = mail
    cliente.direccion = domicilio
    cliente.save()

    total = 0
    for key, value in changuito.iteritems():
        producto = Producto.objects.get(id=key)
        total = total + producto.getPrecioWeb()

    pedido = Pedido()
    pedido.orden_de_venta = pedido.get_next_orden_venta().get('orden_de_venta')
    pedido.cliente = cliente
    pedido.direccion_envio = domicilio
    pedido.telefono = telefono
    pedido.mail = mail
    pedido.metodo_pago = MetodoPago.objects.get(id=5)
    #metodo_envio = models.ForeignKey(MetodoEnvio, null=True, blank=True)
    pedido.armado = User.objects.get(username="web")
    pedido.emitido = User.objects.get(username="web")
    pedido.estado = Estado.objects.get(id=4)
    pedido.total = total
    pedido.punto_venta = PuntoVenta.objects.get(punto_venta="WEB")
    pedido.save()

    if comentario:
        comen = ComentarioPedido()
        comen.comentario = comentario
        comen.pedido = pedido
        comen.save()

    request.session['id_pedido'] = pedido.id

    for key, value in changuito.iteritems():
        producto = Producto.objects.get(id=key)
        productoPedido = ProductoPedido()
        productoPedido.pedido = pedido
        productoPedido.producto = producto
        productoPedido.precio_venta_distribuidor = producto.getPrecioWeb()
        productoPedido.cantidad_productos = value
        productoPedido.total = producto.getPrecioWeb() * value
        productoPedido.save()

    my_strings = json.dumps(urlMP, indent=4) 
    return HttpResponse(urlMP)

def poner_numero_socio(request):
    clientes = Cliente.objects.all()
    numero = 0
    for c in clientes:
        nuevoNumero = str(numero+1)
        cerosCantidad = 5 - len(nuevoNumero)
        ceros = '0' * cerosCantidad
        numeroFinal = ceros + nuevoNumero
        c.numeroSocio = numeroFinal
        c.save()
        numero = numero + 1

    response_data = {}
    response_data['numeroSocio'] = numero
    return HttpResponse(response_data)

def poner_punto_venta(request):
    pedidos = Pedido.objects.all()
    numero = 1
    for p in pedidos:
        p.punto_venta = PuntoVenta.objects.get(id=1)
        p.save()

def compra_completa(request):
    collection_status  = request.GET.get('collection_status', '')

    changoAnterior = get_chango(request)
    changuitoAnterior  = get_changuito(request)
    cantProd, totalProdAnterior = get_chango_valores_total(changuitoAnterior)

    if 'id_pedido' in request.session and request.session['id_pedido'] != "":
        id = request.session['id_pedido']
        pedido = Pedido.objects.get(id=id)
        numeroPedido = pedido.orden_de_venta.split("-")[1]
        numeroSocio  = pedido.cliente.numeroSocio

    if collection_status == "approved":
        request.session['changuito'] = {}
        mensaje = "GRACIAS POR TU COMPRA! YA RECIBIMOS TU PEDIDO."
        collection_id      = request.GET.get('collection_id', '')
        preference_id      = request.GET.get('preference_id', '')
        
        if 'id_pedido' in request.session and request.session['id_pedido'] != "":
            pedido.collection_id = collection_id
            pedido.preference_id = preference_id
            pedido.save()
            request.session['id_pedido'] = ""

    elif collection_status == "pending":
        mensaje = "EL PAGO QUEDO PENDIENTE, ESPERE RECIBIR LA CONFIRMACION DE MERCADOPAGO."
    else:
        mensaje = "EL PAGO NO PUDO COMPLETARSE, COMUNICATE CON NOSOTROS."

    categorias                   = Categoria.objects.filter(shop=True).order_by('orden')
    chango                       = get_chango(request)
    changuito                    = get_changuito(request)
    cantProd, totalProd          = get_chango_valores_total(changuito)
    context = { 'chango':chango,
                'cantProd':cantProd,
                'totalProd':totalProd,
                'changuito':changuito,
                'categorias':categorias,
                'changoAnterior': changoAnterior,
                'totalProdAnterior':totalProdAnterior,
                'mensaje': mensaje,
                'numeroPedido': numeroPedido,
                'numeroSocio': numeroSocio,
            }
    return render(request, 'shop/compra_completa.html', context)

# devuelve los datos de session id:cantidad
def get_changuito(request):
    if 'changuito' in request.session:
        return request.session['changuito']
    else:
        return {}

# devuelve los productos en el chango
def get_chango(request):
    changuito = get_changuito(request)
    if len(changuito) > 0:
        filtro = []
        for k,v in changuito.iteritems():
            filtro.append(int(k))
        return Producto.objects.filter(id__in=filtro)
    else:
        return []

def get_chango_valores_total(changuito):
    cantProd   = 0
    totalProd  = 0
    
    for k,v in changuito.iteritems():
        cantProd  = cantProd + v
        totalProd = totalProd + Producto.objects.get(id=k).getPrecioWeb() * v

    return cantProd, totalProd

def returnUrlMP(request, changuito):
    nombre      = request.POST.get('nombre', '')
    apellido    = request.POST.get('apellido', '')
    mail        = request.POST.get('mail', '')

    lista = []
    for key, value in changuito.iteritems():
        producto = Producto.objects.get(id=key)
        producto.getPrecioWeb()
        item = {
            "title": producto.nombre,
            "quantity": value,
            "currency_id": "ARS",
            "unit_price": producto.getPrecioWeb()
        }
        lista.append(item)

    payer = {
        "name": nombre,
        "surname": apellido,
        "email": mail
    }

    back_urls = {
        "success" : "imperioverdegrowshop.com.ar/shop/compra_completa",
        "pending" : "imperioverdegrowshop.com.ar/shop/compra_completa",
        "failure" : "imperioverdegrowshop.com.ar/shop/compra_completa"
    }

    preference = {
      "items": lista,
      "payer": payer,
      "back_urls": back_urls
    }

    mp = mercadopago.MP("5526799798714434", "t1z7sfLbfnnWhQj95OcAnYu50LFAm8Tb")
    preferenceResult = mp.create_preference(preference)
    url = preferenceResult["response"]["sandbox_init_point"]

    output = """
    <!doctype html>
    <html>
        <head>
            <title>Pagar</title>
        </head>
      <body>
        <a href="{url}" id="MP-Checkout" name="MP-Checkout" class="blue-l-arall-rn">Pagar</a>
        <script type="text/javascript" src="//resources.mlstatic.com/mptools/render.js"></script>
      </body>
    </html>
    """.format (url=url)

    return output

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))

@register.filter
def get_item_aux(dictionary, key):
    return dictionary.get(str(key))


@register.filter
def get_comentario_producto(comentario, id):
    return Producto.objects.get(id=id).comentario()

@register.filter
def multiply(value, arg):
    return value*arg