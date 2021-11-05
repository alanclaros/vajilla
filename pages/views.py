
from utils.dates_functions import get_date_show
from django.db import connection
from django.shortcuts import render

from django.conf import settings
from django.contrib.auth.models import User
# password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib import messages
# reverse
from django.apps import apps
from controllers.SystemController import SystemController

# configuraciones
from src.configuraciones.configuraciones import configuraciones_index
from src.configuraciones.lineas import lineas_index
from src.configuraciones.sucursales import sucursales_index
from src.configuraciones.puntos import puntos_index
from src.configuraciones.usuarios import usuarios_index

# cajas
from src.cajas.cajas_iniciar import cajas_iniciar_index
from src.cajas.cajas_iniciar_recibir import cajas_iniciar_recibir_index
from src.cajas.cajas_entregar import cajas_entregar_index
from src.cajas.cajas_entregar_recibir import cajas_entregar_recibir_index
from src.cajas.cajas_movimientos import cajas_movimientos_index
from src.cajas.cajas_ingresos import cajas_ingresos_index
from src.cajas.cajas_egresos import cajas_egresos_index

# clientes
from src.clientes.clientes import clientes_index
# productos
from src.productos.productos import productos_index

# inventarios
from src.inventarios.ingresos_almacen import ingresos_almacen_index
from src.inventarios.salidas_almacen import salidas_almacen_index
from src.inventarios.movimientos_almacen import movimientos_almacen_index

# ventas
from src.ventas.ventas import ventas_index
from src.ventas.pendientes import pendientes_index

# # reportes
# from src.reportes.reportes import reportes_index
# # recibos
# from src.calendario.lista_cobros import lista_cobros_index


def index(request):
    """pagina index"""

    if 'module_x' in request.POST.keys():
        module_id = int(request.POST['module_x'])

        # cambiar password
        if module_id == 1000:
            return cambiar_password(request)

        if module_id == settings.MOD_CONFIGURACIONES_SISTEMA:
            return configuraciones_index(request)

        if module_id == settings.MOD_LINEAS:
            return lineas_index(request)

        if module_id == settings.MOD_SUCURSALES:
            return sucursales_index(request)

        if module_id == settings.MOD_PUNTOS:
            return puntos_index(request)

        if module_id == settings.MOD_USUARIOS:
            return usuarios_index(request)

        # cajas
        # cajas
        if module_id == settings.MOD_INICIAR_CAJA:
            return cajas_iniciar_index(request)

        if module_id == settings.MOD_INICIAR_CAJA_RECIBIR:
            return cajas_iniciar_recibir_index(request)

        if module_id == settings.MOD_ENTREGAR_CAJA:
            return cajas_entregar_index(request)

        if module_id == settings.MOD_ENTREGAR_CAJA_RECIBIR:
            return cajas_entregar_recibir_index(request)

        if module_id == settings.MOD_CAJAS_INGRESOS:
            return cajas_ingresos_index(request)

        if module_id == settings.MOD_CAJAS_EGRESOS:
            return cajas_egresos_index(request)

        if module_id == settings.MOD_CAJAS_MOVIMIENTOS:
            return cajas_movimientos_index(request)

        # clientes
        if module_id == settings.MOD_CLIENTES:
            return clientes_index(request)

        # productos
        if module_id == settings.MOD_PRODUCTOS:
            return productos_index(request)

        # ingresos almacen
        if module_id == settings.MOD_INGRESOS_ALMACEN:
            return ingresos_almacen_index(request)

        # salidas almacen
        if module_id == settings.MOD_SALIDAS_ALMACEN:
            return salidas_almacen_index(request)

        # movimientos almacen
        if module_id == settings.MOD_MOVIMIENTOS_ALMACEN:
            return movimientos_almacen_index(request)

        # ventas
        if module_id == settings.MOD_VENTAS:
            return ventas_index(request)

        # pendientes
        if module_id == settings.MOD_PENDIENTES:
            return pendientes_index(request)

        context = {
            'module_id': module_id,
        }

        return render(request, 'pages/nada.html', context)

    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'
        usuario = {}

    # # webpush
    # webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    # vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')

    # url_empresa = settings.SUB_URL_EMPRESA

    # # usuarios del sistema para la notificacion
    # status_activo = apps.get_model('status', 'Status').objects.get(pk=1)
    # filtro_usuarios = {}
    # filtro_usuarios['status_id'] = status_activo
    # filtro_usuarios['perfil_id__perfil_id__in'] = [settings.PERFIL_ADMIN, settings.PERFIL_SUPERVISOR, settings.PERFIL_CAJERO]
    # filtro_usuarios['notificacion'] = 1

    # usuarios_notificacion = apps.get_model('permisos', 'UsersPerfiles').objects.filter(**filtro_usuarios).order_by('user_perfil_id')
    # lista_notificacion = ''
    # for usuario_notif in usuarios_notificacion:
    #     lista_notificacion += str(usuario_notif.user_id.id) + '|'

    # if len(lista_notificacion) > 0:
    #     lista_notificacion = lista_notificacion[0:len(lista_notificacion)-1]

    # if settings.SUB_URL_EMPRESA != '':
    #     url_push = '/' + settings.SUB_URL_EMPRESA + '/send_push'
    # else:
    #     url_push = '/send_push'

    context = {
        'autenticado': autenticado,
        'url_notificacion': 'url_notificacion',
        'pagina_inicio': 'si',
        'user': usuario,
        'vapid_key': 'vapid_key',
        'url_empresa': 'url_empresa',
        'lista_notificacion': 'lista_notificacion',
        'url_webpush': 'url_push',
    }

    return render(request, 'pages/index.html', context)

# cambio de password


def cambiar_password(request):
    """cambio de password de los usuarios"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'
        return render(request, 'pages/without_permission.html')

    # por defecto
    usuario_actual = User.objects.get(pk=request.user.id)
    usuario_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=usuario_actual)

    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        # busqueda cliente por ci
        if operation == 'add':
            # verificamos
            error = 0
            password = request.POST['actual'].strip()
            nuevo = request.POST['nuevo'].strip()
            nuevo2 = request.POST['nuevo2'].strip()

            if error == 0 and nuevo == '' and nuevo2 == '':
                error = 1
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Usuario!', 'description': 'Debe llenar su nuevo password y su repeticion'})

            if error == 0 and not check_password(password, usuario_actual.password):
                error = 1
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Usuario!', 'description': 'Error en su password'})

            if error == 0 and nuevo != nuevo2:
                error = 1
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Usuario!', 'description': 'La repeticion de su password no coincide'})

            if error == 0 and len(nuevo) < 6:
                error = 1
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Usuario!', 'description': 'Su nuevo password debe tener al menos 6 letras'})

            if error == 0:
                # actualizamos
                usuario_actual.password = make_password(nuevo)
                usuario_actual.save()
                messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Usuario!', 'description': 'Su nuevo password se cambio correctamente'})

    context = {
        'autenticado': autenticado,
        'usuario_actual': usuario_actual,

        'module_x': 1000,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }

    return render(request, 'pages/cambiar_password.html', context)


def reemplazar_codigo_html(cadena):
    retorno = cadena
    retorno = retorno.replace('&', "&#38;")
    retorno = retorno.replace('#', "&#35;")

    retorno = retorno.replace("'", "&#39;")
    retorno = retorno.replace('"', "&#34;")
    retorno = retorno.replace('á', "&#225;")
    retorno = retorno.replace('é', "&#233;")
    retorno = retorno.replace('í', "&#237;")
    retorno = retorno.replace('ó', "&#243;")
    retorno = retorno.replace('ú', "&#250;")
    retorno = retorno.replace('Á', "&#193;")
    retorno = retorno.replace('É', "&#201;")
    retorno = retorno.replace('Í', "&#205;")
    retorno = retorno.replace('Ó', "&#211;")
    retorno = retorno.replace('Ú', "&#218;")
    retorno = retorno.replace('!', "&#33;")

    retorno = retorno.replace('$', "&#36;")
    retorno = retorno.replace('%', "&#37;")
    retorno = retorno.replace('*', "&#42;")
    retorno = retorno.replace('+', "&#43;")
    retorno = retorno.replace('-', "&#45;")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")

    return retorno


# notificaciones para el usuario
def notificaciones_pagina(request):
    #context = {'abc': 'asdd'}
    # return render(request, 'pages/nada.html', context)

    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    if autenticado == 'no':
        context = {
            'cantidad': 0,
            'cantidad_rojos': 0,
            'notificaciones': {},
            'autenticado': autenticado,
        }
        return render(request, 'pages/notificaciones_pagina.html', context)

    # usuarios autenticados
    try:
        user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)

        lista_notificaciones = []
        cantidad = 0
        cantidad_rojos = 0
        cantidad_normal = 0

        # context para el html
        context = {
            'notificaciones': lista_notificaciones,
            'cantidad': cantidad,
            'cantidad_rojos': cantidad_rojos,
            'cantidad_normal': cantidad_normal,
            'autenticado': autenticado,
        }

        return render(request, 'pages/notificaciones_pagina.html', context)

    except Exception as e:
        print('ERROR ' + str(e))
        context = {
            'cantidad': 0,
            'cantidad_rojos': 0,
            'notificaciones': {},
            'autenticado': autenticado,
        }
        return render(request, 'pages/notificaciones_pagina.html', context)
