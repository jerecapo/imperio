#-*- coding: utf-8 -*-
from django.contrib import admin, messages
from django import forms
from .models import Estado, MetodoEnvio, MetodoPago, Cliente, Producto, Pedido, ProductoPedido, ComentarioPedido, ComentarioCliente, ComentarioProducto, EtiquetasProducto, Categoria, Gasto, Proveedor, TipoGasto, ImagenProducto, PuntoVenta
from django.contrib.sessions.models import Session

class ComentarioProductoInline(admin.TabularInline):
    model = ComentarioProducto
    extra = 0

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 0

class ProductoPedidoInline(admin.TabularInline):
    model = ProductoPedido
    extra = 0
    
class ComentarioPedidoInline(admin.TabularInline):
    model = ComentarioPedido
    extra = 0
    
class ComentarioClienteInline(admin.TabularInline):
    model = ComentarioCliente
    extra = 0

class EtiquetasProductoInline(admin.TabularInline):
    model = EtiquetasProducto
    extra = 0

class PedidoForm(forms.ModelForm):
    
    class Media:
       js = ('admin/js/vendor/jquery/jquery.js', 'admin/js/custom_admin_validate.js')
    
class PedidoAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_per_page = 400
    form = PedidoForm
    inlines = [
        ProductoPedidoInline, ComentarioPedidoInline
    ]
    fieldsets = (
        ('Principal', {
            'classes': ('wide', 'extrapretty'),
            'fields': ['orden_de_venta', 'fecha']
        }),
        ('Cliente', {
            'fields': ['cliente', 'direccion_envio', 'mail', 'telefono']
        }),

        ('Logistica', {
            'fields': ['metodo_pago', 'metodo_envio', 'armado', 'emitido','punto_venta']
        }),
        ('Estado y Total', {
            'fields': ['estado', 'total']
        }),
        ('MP', {
            'classes': ('collapse',),
            'fields': ['collection_id', 'preference_id']
        }),
    )
    list_display =  ('orden_de_venta', 'fecha', 'total','cliente','punto_venta','metodo_pago','metodo_envio', 'estado','button','collection_id', 'preference_id')
    
    def save_model(self, request, obj, form, change):

        try:
            p = Pedido.objects.get(pk = obj.id)
            if p.estado.id == 5 and obj.estado.id == 11:
                #devolverStock()
                for pp in obj.productopedido_set.all():
                    stock = pp.cantidad_productos
                    producto = pp.producto
                    producto.stocks = producto.stocks + stock
                    producto.save()
                mensaje = "Se devolvio el stock por CANCELAR el pedido."      
            elif p.estado.id != 11 and p.estado.id != 5 and obj.estado.id == 5:
                #restarStock()
                for pp in obj.productopedido_set.all():
                    stock = pp.cantidad_productos
                    producto = pp.producto
                    producto.stocks = producto.stocks - stock
                    producto.save()
                mensaje = "Se resto el stock por FINALIZAR el pedido."
            else:
                mensaje = ""   
        except Pedido.DoesNotExist:  
            mensaje = "" 
        except Exception as e:
            mensaje = "Error, mostrale este mensaje a Jere: " + str(e) 

        if mensaje != "":
            messages.success(request, mensaje)  

        obj.save()
        
    
    def get_changeform_initial_data(self, request):
        try:
            pedidoUno = Pedido.objects.order_by('-orden_de_venta')[0].orden_de_venta
            pedido = pedidoUno.split('-')[1]
            nuevoNumero = str(int(pedido)+1)
            cerosCantidad = 7 - len(nuevoNumero)
            ceros = '0' * cerosCantidad
            pedido = pedidoUno.split('-')[0] + '-' + ceros + nuevoNumero
        except:
            pedido = '0001-0000001'

        return {'orden_de_venta': pedido}
        
    
class ClienteAdmin(admin.ModelAdmin):
    list_max_show_all = 10000
    list_per_page = 10000
    inlines = [
        ComentarioClienteInline,
    ]
    list_display = ('id', 'cliente', 'numeroSocio', 'contacto', 'telefono', 'celular','email', 'direccion', 'fecha')
    fieldsets = (
        ('Principal', {
            'classes': ('wide', 'extrapretty'),
            'fields': ['cliente', 'contacto']
        }),
        ('Cliente', {
            'fields': ['numeroSocio', 'telefono', 'celular', 'email', 'direccion']
        }),
        ('Fecha de entrada', {
            'fields': ['fecha'] 
        }),
    )
    
class ProductoAdmin(admin.ModelAdmin):
    list_max_show_all = 10000
    list_per_page = 10000
    inlines = [
        ComentarioProductoInline, EtiquetasProductoInline, ImagenProductoInline
    ]
    list_display = ('nombre', 'categoria', 'precio_costo', 'precio_venta_distribuidor','precio_venta_publico','stocks','shop','oferta','destacado')
    fieldsets = (
        ('Principal', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('nombre', 'categoria', 'precio_costo', 'precio_venta_distribuidor','precio_venta_publico','stocks','shop','oferta','destacado')
        }),
    )

class ProveedorAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_per_page = 400

    list_display = ('proveedor', 'contacto', 'telefono','celular', 'email', 'direccion', 'fecha')
    fieldsets = (
        ('Principal', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('proveedor', 'contacto', 'telefono','celular', 'email', 'direccion', 'fecha')
        }),
    )
    
class GastoAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_per_page = 400

    list_display = ('fecha', 'autorizado','proveedor', 'metodo_pago', 'tipo_gasto', 'total')
    fieldsets = (
        ('Principal', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('fecha', 'autorizado','proveedor', 'metodo_pago', 'tipo_gasto', 'total', 'comentario')
        }),
    )
    
class CategoriaAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_per_page = 400

    list_display = ('nombre', 'orden','shop')
    fieldsets = (
        ('Principal', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('nombre', 'orden','shop')
        }),
    )

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']

admin.site.register(Session, SessionAdmin)

admin.site.register(PuntoVenta)
admin.site.register(TipoGasto)
admin.site.register(Estado)
admin.site.register(MetodoEnvio)
admin.site.register(MetodoPago)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Gasto, GastoAdmin)
admin.site.register(Proveedor, ProveedorAdmin)