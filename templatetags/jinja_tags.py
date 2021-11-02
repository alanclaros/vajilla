from datetime import datetime
from django import template
from django.conf import settings
from django.apps import apps

from utils.dates_functions import get_date_show

from controllers.SystemController import SystemController

from datetime import datetime, timedelta, date

register = template.Library()
system_controller = SystemController()


@register.filter('get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter('get_objeto_user_modulo')
def get_objeto_user_modulo(key, lista_user_modulo):
    for user_modulo in lista_user_modulo:  # lista de objectos
        if key == user_modulo.modulo_id.modulo_id:  # atributos del objecto
            return user_modulo.__dict__


@register.filter('back_class')
def back_class(index):
    """combinacion de color de filas"""
    if int(index) % 2 == 0:
        return '1'
    else:
        return '2'


@register.filter('back_class_color')
def back_class_color(index, estado):
    """combinacion de color de filas segun estado"""
    estado_int = int(estado)

    if estado_int == settings.STATUS_ANULADO:
        return 'anulado'

    if estado_int == settings.STATUS_INACTIVO:
        return 'inhabil'

    if estado_int == settings.STATUS_PREVENTA:
        return 'cobrado'

    if estado_int == settings.STATUS_VENTA:
        return 'venta'

    if estado_int == settings.STATUS_SALIDA_ALMACEN:
        return 'salida'

    if estado_int == settings.STATUS_VUELTA_ALMACEN:
        return 'vuelta'

    if estado_int == settings.STATUS_FINALIZADO:
        return 'finalizado'

    if int(index) % 2 == 0:
        return '1'
    else:
        return '2'


@register.filter('fecha_mostrar')
def fecha_mostrar(fecha, formato):
    if fecha:
        return get_date_show(fecha, formato=formato)

    else:
        return '/N'


# get cantidad apertura detalle, cajas operacioens detalles
@register.filter('get_cantidad_apertura')
def get_cantidad_apertura(moneda_id, cajas_operaciones_detalles):
    for detalle in cajas_operaciones_detalles:
        if moneda_id == detalle.moneda_id.moneda_id:
            return detalle.cantidad_apertura

    return ''


@register.filter('get_cantidad_cierre')
def get_cantidad_cierre(moneda_id, cajas_operaciones_detalles):
    for detalle in cajas_operaciones_detalles:
        if moneda_id == detalle.moneda_id.moneda_id:
            return detalle.cantidad_cierre

    return ''


# # verificamos si la fecha es de hoy
# @register.filter('is_today')
# def is_today(fecha):
#     retorno = 'n'
#     anio = datetime.now().year
#     mes = datetime.now().month
#     dia = datetime.now().day

#     if type(fecha) == datetime:
#         f_anio = fecha.year
#         f_mes = fecha.month
#         f_dia = fecha.day

#         if f_anio == anio and f_mes == mes and f_dia == dia:
#             retorno = 'y'

#     return retorno


# caja get
@register.filter('get_caja')
def get_caja(Cajas_lista, caja_id):
    for caja in Cajas_lista:
        if caja.caja_id == caja_id:
            return caja.codigo

    return ''


# caja punto
@register.filter('get_punto')
def get_punto(Puntos_lista, punto_id):
    for punto in Puntos_lista:
        if punto.punto_id == punto_id:
            return punto.punto

    return ''


# punto del usuario
@register.filter('get_punto_user')
def get_punto_user(user):
    retorno = ''
    try:
        if system_controller.model_exits('UsersPerfiles'):
            user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=user)
            punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)

            return punto.punto
    except Exception as ex:
        retorno = ''

    return retorno


# permiso para el grupo
@register.filter('lista_modulos')
def lista_modulos(user):
    modulos_usuario = []
    try:
        user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=user)

        if system_controller.model_exits('UsersModulos'):
            modulos_usuario = apps.get_model('permisos', 'UsersModulos').objects.filter(user_perfil_id=user_perfil)
    except Exception as ex:
        print('permisos no instalado')

    return modulos_usuario


# permisos del usuario
@register.filter('permisos_modulo')
def permisos_modulo(modulos_usuario, modulos):
    lista = str(modulos)
    div = lista.split(',')

    permiso = 'no'
    for mod in div:
        for mu in modulos_usuario:
            if int(mod) == int(mu.modulo_id.modulo_id):
                if mu.enabled:
                    permiso = 'si'

    return permiso


# # devolviendo el objeto usuario perfil del usuario
# @register.filter('get_status_user')
# def get_status_user(usuarios_perfiles, usuario):
#     retorno = 0
#     for usuario_perfil in usuarios_perfiles:
#         if usuario_perfil.user_id == usuario:
#             retorno = usuario_perfil.status_id.status_id

#     return retorno


# verificando si el almacen esta registrado en puntos almacenes
@register.filter('verificar_punto_almacen')
def verificar_punto_almacen(almacen, lista_punto_almacen):
    retorno = 'no'
    for punto_almacen in lista_punto_almacen:
        if punto_almacen.almacen_id == almacen:
            retorno = 'si'

    return retorno


@register.filter('get_sub_url_empresa')
def get_sub_url_empresa(empresa):
    retorno = ''
    if settings.CURRENT_HOST == '127.0.0.1':
        retorno = ''
    else:
        if settings.SUB_URL_EMPRESA == 'ventas_renekris':
            retorno = ''
        else:
            retorno = '/' + settings.SUB_URL_EMPRESA

    if empresa:
        return retorno
    else:
        return ''


# @register.filter('get_forloop_menos1')
# def get_forloop_menos1(forloop_number):
#     retorno = int(forloop_number) - 1

#     return retorno


@register.filter('toint')
def toint(number):
    try:
        retorno = int(number)
    except Exception as ex:
        retorno = ''

    return retorno


@register.filter('venta_to_gastos')
def venta_to_gastos(estado, tipo):
    try:
        retorno = 0
        if tipo == 'add_gasto' or tipo == 'add_cobro':
            if estado in [settings.STATUS_VENTA, settings.STATUS_SALIDA_ALMACEN, settings.STATUS_VUELTA_ALMACEN]:
                retorno = 1
        if tipo == 'add_items':
            if estado in [settings.STATUS_VENTA, settings.STATUS_SALIDA_ALMACEN]:
                retorno = 1
    except Exception as ex:
        retorno = 0

    return retorno


@register.filter('subtract')
def subtract(num1, num2):
    return num1 - num2


@register.filter('detalle_venta')
def detalle_venta(venta_detalles, fila):
    #print('venta detalles: ', venta_detalles, ' fila: ', fila)
    #print('pos cero: ', venta_detalles[0])
    datos = {}
    datos['producto_id'] = '0'
    datos['producto'] = ''
    datos['cantidad_salida'] = ''
    datos['costo_salida'] = ''
    datos['total_salida'] = ''
    datos['detalle'] = ''
    if venta_detalles is None:
        return datos

    tam = len(venta_detalles)
    #print('tam: ', tam)
    if fila <= tam:
        #print('fila menor a tamaño: ', fila, ' tam: ', tam)
        datos['producto_id'] = venta_detalles[fila-1].producto_id.producto_id
        datos['producto'] = venta_detalles[fila-1].producto_id.linea_id.linea + ' - ' + venta_detalles[fila-1].producto_id.producto
        datos['cantidad_salida'] = venta_detalles[fila-1].cantidad_salida
        datos['costo_salida'] = venta_detalles[fila-1].costo_salida
        datos['total_salida'] = venta_detalles[fila-1].total_salida
        datos['detalle'] = venta_detalles[fila-1].detalle

    #print('datos jinja: ', datos)
    return datos


@register.filter('get_stock')
def get_stock(lista_stock, producto_id):
    return lista_stock[producto_id]


@register.filter('get_aumento_detalle')
def get_aumento_detalle(aumento):
    detalles = []
    try:
        venta_aumento_detalles = apps.get_model('ventas', 'VentasAumentosDetalles').objects.filter(venta_aumento_id=aumento)
        for detalle in venta_aumento_detalles:
            dato = {}
            dato['producto'] = detalle.producto_id.linea_id.linea + ' - ' + detalle.producto_id.producto
            dato['cantidad_salida'] = detalle.cantidad_salida
            dato['costo_salida'] = detalle.costo_salida
            dato['total_salida'] = detalle.total_salida
            dato['detalle'] = detalle.detalle
            detalles.append(dato)

        #print('detalles: ', detalles)
        return detalles
    except Exception as ex:
        return []


@register.filter('total_producto_vuelta')
def total_producto_vuelta(producto):
    retorno = 0
    try:
        retorno = ((producto['cantidad_salida'] - producto['cantidad_vuelta']) * producto['costo_rotura']) + producto['refaccion']
        retorno = round(retorno, 2)
        return retorno
    except Exception as ex:
        return retorno
