from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.template.defaulttags import register
from ventas.models import Producto, Categoria

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

    context = { 'mensaje': mensaje,
                'categorias':categorias,
                'producto':producto,
                'changuito':changuito,
                'chango':chango,
                'cantProd':cantProd,
                'totalProd':totalProd,
                'adicTarjeta':adicTarjeta,
                'totalConTarjeta':totalConTarjeta,
            }
    return render(request, 'shop/carretilla.html', context)

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
        totalProd = totalProd + Producto.objects.get(id=k).precio_venta_publico * v

    return cantProd, totalProd

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))

@register.filter
def get_comentario_producto(comentario, id):
    return Producto.objects.get(id=id).comentario()

@register.filter
def multiply(value, arg):
    return value*arg