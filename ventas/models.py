#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_unicode

import datetime  

class Categoria(models.Model):
    nombre = models.CharField('Nombre', max_length=250)
    orden  = models.IntegerField('Orden', default=0)
    shop   = models.BooleanField('Shop', default=False)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorias" 

class Estado(models.Model):
    nombre = models.CharField('Nombre', max_length=250)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Estados" 

class MetodoEnvio(models.Model):
    metodo_envio = models.CharField('Metodo envio', max_length=150)
    
    def __str__(self):
        return self.metodo_envio

    class Meta:
        verbose_name_plural = "Metodos de Envio" 

class MetodoPago(models.Model):
    metodo_pago = models.CharField('Metodo pago', max_length=20)
    
    def __str__(self):
        return self.metodo_pago

    class Meta:
        verbose_name_plural = "Metodos de Pago" 

class TipoGasto(models.Model):
    tipo_gasto = models.CharField('Tipo de Gasto', max_length=30)
    
    def __str__(self):
        return self.tipo_gasto

    class Meta:
        verbose_name_plural = "Tipos de gasto" 
        
class Cliente(models.Model):
    cliente = models.CharField('Cliente', max_length=100)
    contacto = models.CharField('Contacto', max_length=100)
    telefono = models.CharField('Telefono', max_length=20, null=True, blank=True)
    celular = models.CharField('Celular', max_length=20, null=True, blank=True)
    email = models.CharField('Email', max_length=100, null=True, blank=True)
    direccion = models.CharField('Direccion', max_length=200, null=True, blank=True)
    fecha = models.DateTimeField('Fecha entrada',default=datetime.datetime.now)
    
    def __str__(self):
        return self.cliente + " (" + str(self.id) + ")"

    class Meta:
        verbose_name_plural = "Clientes" 
        ordering = ('cliente',)

class Proveedor(models.Model):
    proveedor = models.CharField('Proveedor', max_length=100)
    contacto = models.CharField('Contacto', max_length=100, null=True, blank=True)
    telefono = models.CharField('Telefono', max_length=20, null=True, blank=True)
    celular = models.CharField('Celular', max_length=20, null=True, blank=True)
    email = models.CharField('Email', max_length=100, null=True, blank=True)
    direccion = models.CharField('Direccion', max_length=200, null=True, blank=True)
    fecha = models.DateTimeField('Fecha entrada',default=datetime.datetime.now)
    
    def __str__(self):
        return self.proveedor

    class Meta:
        verbose_name_plural = "Proveedores" 
        ordering = ('proveedor',)
        
class Producto(models.Model):
    nombre = models.CharField('Nombre', max_length=250)
    categoria = models.ForeignKey(Categoria, null=True, blank=True)
    precio_venta_distribuidor = models.FloatField('Precio Venta Distribuidor',default=0)
    precio_venta_publico = models.FloatField('Precio Venta Publico',default=0)
    precio_costo = models.FloatField('Precio Costo',default=0)
    stocks = models.FloatField('Stock',default=0)
    shop = models.BooleanField('Shop', default=False)
    oferta = models.BooleanField('Oferta', default=False)
    destacado = models.BooleanField('Destacado', default=False)
    
    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
        return self.nombre

    def comentario(self):
        if len(self.comentarioproducto_set.all()) > 0:
            return self.comentarioproducto_set.all()[0].comentario
        else:
            return 'SIN COMENTARIOS.'


    def dameFotoPrincipal(self):
        if len(self.imagenproducto_set.all()) > 0:
            imagen = self.imagenproducto_set.all().order_by('-principal')[0].imagen.url
        else:
            imagen = '/static/shop/img/product/7.jpg'
        return imagen

    def dameFotoOferta(self):
        if len(self.imagenproducto_set.all()) > 0:
            imagen = self.imagenproducto_set.all().order_by('-principal')[0].imagen.url
        else:
            imagen = '/static/shop/img/banner/2.jpg'
        return imagen

    def dameFotoChango(self):
        if len(self.imagenproducto_set.all()) > 0:
            imagen = self.imagenproducto_set.all().order_by('-principal')[0].imagen.url
        else:
            imagen = '/static/shop/img/cart/1.jpg'
        return imagen

    def dameFotosShop(self):
        return self.imagenproducto_set.all().order_by('-principal')
        

    class Meta:
        verbose_name_plural = "Productos" 
        ordering = ('nombre',)

class EtiquetasProducto(models.Model):
    producto = models.ForeignKey(Producto)
    etiqueta = models.ImageField(upload_to="etiquetas/")
    nombre = models.CharField('Nombre', max_length=250)
    comentario = models.TextField('Comentario', null=True, blank=True)

class Gasto(models.Model):
    fecha = models.DateTimeField('Fecha gasto',default=datetime.datetime.now)
    autorizado = models.ForeignKey(User)
    proveedor = models.ForeignKey(Proveedor)
    metodo_pago = models.ForeignKey(MetodoPago, null=True, blank=True)
    tipo_gasto = models.ForeignKey(TipoGasto)
    total = models.FloatField('Total',default=0)
    comentario = models.TextField('Comentario', null=True, blank=True)
    
    def __unicode__(self):
        return u'%s' % self.proveedor.proveedor

    def __str__(self):
        return self.proveedor.proveedor
        
    class Meta:
        verbose_name_plural = "Gastos del dia" 
    
class Pedido(models.Model):
    orden_de_venta = models.CharField('Orden de Venta', max_length=50)
    fecha = models.DateTimeField('Fecha pedido',default=datetime.datetime.now)
    cliente = models.ForeignKey(Cliente)
    direccion_envio = models.CharField('Direccion envio', max_length=250)
    telefono = models.CharField('Telefono', max_length=50, null=True, blank=True)
    mail = models.CharField('Mail', max_length=100, null=True, blank=True)
    metodo_pago = models.ForeignKey(MetodoPago, null=True, blank=True)
    metodo_envio = models.ForeignKey(MetodoEnvio, null=True, blank=True)
    armado = models.ForeignKey(User, null=True, blank=True, related_name='armado_por')
    emitido = models.ForeignKey(User, null=True, blank=True, related_name='emitido_por')
    estado = models.ForeignKey(Estado)
    total = models.FloatField('Total',default=0)

    def button(self):
        return mark_safe('<a href="/imprimir?pedido_id=%s" target="_blank">Imprimir</a>' %self.id)
    
    def __unicode__(self):
        return u'%s' % self.orden_de_venta

    def __str__(self):
        return self.orden_de_venta
        
    def get_default_orden_de_venta():
        pedido = Pedido.objects.order_by('-orden_de_venta')[0]
        return pedido.orden_de_venta

    def save(self, *args, **kwargs):
        total = 0
        for pp in self.productopedido_set.all():
            total = total + pp.total
            
        self.total = total

        super(Pedido, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Ventas del dia" 
        

class ProductoPedido(models.Model):
    pedido = models.ForeignKey(Pedido)
    producto = models.ForeignKey(Producto)
    precio_venta_distribuidor = models.FloatField('Precio',default=0)
    cantidad_productos = models.FloatField('Cantidad',default=0)
    descuento = models.FloatField('Descuento',default=0)
    total = models.FloatField('Total',default=0)
    comentario = models.CharField('Comentario', max_length=250, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.producto.nombre
    
    def __str__(self):
        return self.producto.nombre

    class Meta:
        verbose_name_plural = "Articulos del Pedido"         

class ComentarioPedido(models.Model):
    comentario = models.TextField('Comentario')
    pedido = models.ForeignKey(Pedido)
    fecha = models.DateTimeField('Fecha',default=datetime.datetime.now)
    principal = models.BooleanField('Principal', default=False)

    def __str__(self):
        return self.comentario

    class Meta:
        verbose_name_plural = "Comentarios Pedido" 
        
class ComentarioCliente(models.Model):
    comentario = models.TextField('Comentario')
    cliente = models.ForeignKey(Cliente)
    fecha = models.DateTimeField('Fecha',default=datetime.datetime.now)
    
    def __str__(self):
        return self.comentario

    class Meta:
        verbose_name_plural = "Comentarios Cliente" 
        
class ComentarioProducto(models.Model):
    comentario = models.TextField('Comentario')
    producto = models.ForeignKey(Producto)
    fecha = models.DateTimeField('Fecha',default=datetime.datetime.now)
    
    def __str__(self):
        return self.comentario

    class Meta:
        verbose_name_plural = "Comentarios Producto" 

class ImagenProducto(models.Model):
    imagen   = models.FileField(upload_to='imgProd/')
    producto = models.ForeignKey(Producto)
    principal = models.BooleanField('Principal', default=False)

    def __str__(self):
        return self.producto.nombre

    class Meta:
        verbose_name_plural = "Imagenes Producto" 

class Stock(models.Model):
    producto = models.ForeignKey(Producto)
    fecha = models.DateTimeField('Fecha',default=datetime.datetime.now)
    inicial = models.IntegerField('Inicial',default=0)
    actual = models.IntegerField('Actual',default=0)

    def __str__(self):
        return self.producto.nombre

    class Meta:
        verbose_name_plural = "Stock" 
