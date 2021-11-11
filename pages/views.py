
import os
from utils.dates_functions import add_minutes_datetime, get_date_show, get_date_to_db, get_fecha_int, get_minutes_date1_sub_date2
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

# reportes
from src.reportes.reportes import reportes_index
from utils.permissions import current_date, get_permissions_user, get_system_settings, get_user_permission_operation
from datetime import datetime
# xls
import openpyxl
from decimal import Decimal
import zipfile
from django.http import FileResponse, HttpResponse
# conexion directa a la base de datos
from django.db import connection


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

        # reportes
        if module_id == settings.MOD_REPORTES:
            return reportes_index(request)

        # backup
        if module_id == settings.MOD_TABLAS_BACKUP:
            return backup(request)

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

    # webpush
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')

    url_empresa = settings.SUB_URL_EMPRESA

    # usuarios del sistema para la notificacion
    status_activo = apps.get_model('status', 'Status').objects.get(pk=1)
    filtro_usuarios = {}
    filtro_usuarios['status_id'] = status_activo
    filtro_usuarios['perfil_id__perfil_id__in'] = [settings.PERFIL_ADMIN, settings.PERFIL_SUPERVISOR, settings.PERFIL_ALMACEN, settings.PERFIL_CAJERO]
    filtro_usuarios['notificacion'] = 1

    usuarios_notificacion = apps.get_model('permisos', 'UsersPerfiles').objects.filter(**filtro_usuarios).order_by('user_perfil_id')
    lista_notificacion = ''
    for usuario_notif in usuarios_notificacion:
        lista_notificacion += str(usuario_notif.user_id.id) + '|'

    if len(lista_notificacion) > 0:
        lista_notificacion = lista_notificacion[0:len(lista_notificacion)-1]

    if settings.SUB_URL_EMPRESA != '':
        url_push = '/' + settings.SUB_URL_EMPRESA + '/send_push'
    else:
        url_push = '/send_push'

    context = {
        'autenticado': autenticado,
        'url_notificacion': 'url_notificacion',
        'pagina_inicio': 'si',
        'user': usuario,
        'vapid_key': vapid_key,
        'url_empresa': url_empresa,
        'lista_notificacion': lista_notificacion,
        'url_webpush': url_push,
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


def backup(request):
    """backup"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'
        return render(request, 'pages/without_permission.html')

    if not get_user_permission_operation(request.user, settings.MOD_TABLAS_BACKUP, 'lista'):
        return render(request, 'pages/without_permission.html')

    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        lista_tablas = [['auth', 'User', 'auth_user'], ['status', 'Status', 'status'],

                        ['permisos', 'Perfiles', 'perfiles'], ['permisos', 'Modulos', 'modulos'], ['permisos', 'UsersPerfiles', 'users_perfiles'], ['permisos', 'UsersModulos', 'users_modulos'],

                        ['configuraciones', 'Configuraciones', 'configuraciones'], ['configuraciones', 'Paises', 'paises'], ['configuraciones', 'Ciudades', 'ciudades'], ['configuraciones', 'Sucursales', 'sucursales'],
                        ['configuraciones', 'Puntos', 'puntos'], ['configuraciones', 'TiposMonedas', 'tipos_monedas'], ['configuraciones', 'Monedas', 'monedas'],
                        ['configuraciones', 'Cajas', 'cajas'], ['configuraciones', 'Almacenes', 'almacenes'], ['configuraciones', 'Lineas', 'lineas', 'puntos_almacenes'],

                        ['cajas', 'CajasIngresos', 'cajas_ingresos'], ['cajas', 'CajasEgresos', 'cajas_egresos'], ['cajas', 'CajasOperaciones', 'cajas_operaciones'],
                        ['cajas', 'CajasOperacionesDetalles', 'cajas_operaciones_detalles'], ['cajas', 'CajasMovimientos', 'cajas_movimientos'],

                        ['clientes', 'Clientes', 'clientes'],

                        ['productos', 'Productos', 'productos'], ['productos', 'ProductosImagenes', 'productos_imagenes'], ['productos', 'ProductosRelacionados', 'productos_relacionados'],

                        ['inventarios', 'Registros', 'registros'], ['inventarios', 'RegistrosDetalles', 'registros_detalles'], ['inventarios', 'Stock', 'stock'],

                        ['ventas', 'Ventas', 'ventas'], ['ventas', 'VentasDetalles', 'ventas_detalles'], ['ventas', 'VentasAumentos', 'ventas_aumentos'], ['ventas', 'VentasAumentosDetalles', 'ventas_aumentos_detalles']
                        ]

        if operation == 'add':
            # leemos las tablas y realizamos la copia
            wb = openpyxl.Workbook()
            # creamos las hojas
            for tabla in lista_tablas:
                ws = wb.create_sheet(tabla[2])
                modelo = apps.get_model(tabla[0], tabla[1])

                # print('modelo...: ', modelo)
                # for field in modelo._meta.fields:
                #     columna = field.get_attname_column()
                #     print('columna: ', columna)

                #columna = modelo._meta.get_field(arg)
                #ws.append(('111', '22222'))

                # columnas = modelo._meta.fields
                # print('columnas...: ', len(columnas))

                aux_columnas = modelo._meta.fields
                len_columnas = len(aux_columnas)

                lista_filas = []
                lista_select = ''
                for field in modelo._meta.fields:
                    #columna = field[1]
                    #print('columna: ', columna)
                    columna = field.get_attname_column()
                    nombre_columna = columna[1]
                    lista_filas.append(nombre_columna)
                    lista_select += nombre_columna + ','

                if len(lista_select) > 0:
                    lista_select = lista_select[0:len(lista_select)-1]

                # titulos columnas
                ws.append(lista_filas)

                # datos
                nombre_tabla = tabla[2]
                sql = f"SELECT {lista_select} FROM {nombre_tabla} "
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    for row in rows:
                        fila = []
                        for i in range(len_columnas):
                            #print('i...: ', i)
                            fila.append(row[i])

                        # aniadimos la fila
                        ws.append(fila)

            # response = HttpResponse(content_type="application/msexcel")
            # response["Content-Disposition"] = "attachment; filename=backup.xlsx"
            # wb.save(response)
            # return response
            ruta_settings = settings.STATICFILES_DIRS[0]
            ruta_guardar = os.path.join(ruta_settings, 'img', 'files_download', 'backup.xlsx')
            loczip = os.path.join(ruta_settings, 'img', 'files_download', 'backup.zip')

            # eliminamos archivos si es que existen
            if os.path.isfile(ruta_guardar):
                os.unlink(ruta_guardar)
            if os.path.isfile(loczip):
                os.unlink(loczip)

            wb.save(ruta_guardar)
            wb.close()

            zip = zipfile.ZipFile(loczip, "w")
            # con path
            # zip.write(ruta_guardar)
            # quitando el path
            zip.write(ruta_guardar, os.path.basename(ruta_guardar))
            zip.close()

            zip_file = open(loczip, 'rb')
            return FileResponse(zip_file)

            # print('zip fileee....: ', zip_file)
            # response = HttpResponse(zip_file, content_type='application/force-download')
            # print('response...: ', response)
            # response['Content-Disposition'] = 'attachment; filename="%s"' % 'backup.zip'
            # return response

    context = {
        'autenticado': autenticado,
        'url_main': '',
        'module_x': settings.MOD_TABLAS_BACKUP,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }

    return render(request, 'pages/backup.html', context)


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
        listado = lista_para_notificar(request.user)

        # context para el html
        context = {
            'notificaciones': listado['lista_notificaciones'],
            'cantidad': listado['cantidad'],
            'cantidad_danger': listado['cantidad_danger'],
            'cantidad_warning': listado['cantidad_warning'],
            'autenticado': autenticado,
        }

        return render(request, 'pages/notificaciones_pagina.html', context)

    except Exception as e:
        print('ERROR ' + str(e))
        context = {
            'cantidad': 0,
            'cantidad_danger': 0,
            'cantidad_warning': 0,
            'notificaciones': {},
            'autenticado': autenticado,
        }
        return render(request, 'pages/notificaciones_pagina.html', context)


# notificaciones push para el usuario
def notificaciones_push(request):
    autenticado = 'no'
    if 'keypush' in request.GET.keys():
        key_push = request.GET['keypush']
        if key_push == settings.KEY_PUSH:
            autenticado = 'si'

    if autenticado == 'no':
        return render(request, 'pages/without_permission.html', {})

    # usuarios autenticados
    try:
        user_adm = User.objects.get(pk=1)
        listado = lista_para_notificar(user_adm)

        lista_entregar = ''
        lista_recoger = ''
        lista_finalizar = ''
        for notificacion in listado['lista_notificaciones']:
            if notificacion['tipo'] == 'E':
                lista_entregar += notificacion['tipo_notificacion'] + '|' + notificacion['descripcion'] + '||'

            if notificacion['tipo'] == 'R':
                lista_recoger += notificacion['tipo_notificacion'] + '|' + notificacion['descripcion'] + '||'

            if notificacion['tipo'] == 'F':
                lista_finalizar += notificacion['tipo_notificacion'] + '|' + notificacion['descripcion'] + '||'

        if len(lista_entregar) > 0:
            lista_entregar = lista_entregar[0:len(lista_entregar)-2]

        if len(lista_recoger) > 0:
            lista_recoger = lista_recoger[0:len(lista_recoger)-2]

        if len(lista_finalizar) > 0:
            lista_finalizar = lista_finalizar[0:len(lista_finalizar)-2]

        # lista de usuarios para mandar notificaciones
        status_activo = apps.get_model('status', 'Status').objects.get(pk=1)
        lista_user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.filter(status_id=status_activo, notificacion=1)
        lista_up_admin = ''
        lista_up_supervisor = ''
        lista_up_almacen = ''
        lista_up_cajero = ''

        for user_perfil in lista_user_perfil:
            if user_perfil.perfil_id.perfil_id == settings.PERFIL_ADMIN:
                lista_up_admin += str(user_perfil.user_id.id) + '|'

            if user_perfil.perfil_id.perfil_id == settings.PERFIL_SUPERVISOR:
                lista_up_supervisor += str(user_perfil.user_id.id) + '|'

            if user_perfil.perfil_id.perfil_id == settings.PERFIL_ALMACEN:
                lista_up_almacen += str(user_perfil.user_id.id) + '|'

            if user_perfil.perfil_id.perfil_id == settings.PERFIL_CAJERO:
                lista_up_cajero += str(user_perfil.user_id.id) + '|'

        #print('lista up admin: ', lista_up_admin)
        if len(lista_up_admin) > 0:
            lista_up_admin = lista_up_admin[0:len(lista_up_admin)-1]

        if len(lista_up_supervisor) > 0:
            lista_up_supervisor = lista_up_supervisor[0:len(lista_up_supervisor)-1]

        if len(lista_up_almacen) > 0:
            lista_up_almacen = lista_up_almacen[0:len(lista_up_almacen)-1]

        if len(lista_up_cajero) > 0:
            lista_up_cajero = lista_up_cajero[0:len(lista_up_cajero)-1]

        # webpush
        webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
        vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
        if settings.CURRENT_HOST == '127.0.0.1':
            url_push = '/send_push'
        else:
            url_push = '/' + settings.SUB_URL_EMPRESA + '/send_push'

        # context para el html
        context = {
            'url_push': url_push,
            'lista_up_admin': lista_up_admin,
            'lista_up_supervisor': lista_up_supervisor,
            'lista_up_cajero': lista_up_cajero,
            'lista_up_almacen': lista_up_almacen,
            'vapid_key': vapid_key,
            'lista_entregar': lista_entregar,
            'lista_recoger': lista_recoger,
            'lista_finalizar': lista_finalizar,
        }

        return render(request, 'pages/notificaciones_push.html', context)

    except Exception as e:
        print('ERROR ' + str(e))
        context = {
            'lista_up_admin': '',
            'lista_up_supervisor': '',
            'lista_up_cajero': '',
            'lista_up_almacen': '',
            'vapid_key': '',
        }
        return render(request, 'pages/notificaciones_push.html', context)


def lista_para_notificar(user):
    # usuarios autenticados
    retorno = {}
    lista_notificaciones = []
    cantidad = 0
    cantidad_danger = 0
    cantidad_warning = 0

    try:
        # ventas que se tienen que entregar
        hora = '0' + str(datetime.now().hour) if len(str(datetime.now().hour)) == 1 else str(datetime.now().hour)
        minuto = '0' + str(datetime.now().minute) if len(str(datetime.now().minute)) == 1 else str(datetime.now().minute)
        segundo = '0' + str(datetime.now().second) if len(str(datetime.now().second)) == 1 else str(datetime.now().second)

        fecha_actual = current_date() + ' ' + hora + ':' + minuto + ':' + segundo
        fecha_actual_int = get_fecha_int(fecha_actual)

        configuraciones_db = get_system_settings()
        #print('configuraciones db: ', configuraciones_db)
        tiempo_aviso_entrega = configuraciones_db['minutos_aviso_entregar']  # 6*60  # minutos, 6 horas
        tiempo_aviso_entrega_tarde = configuraciones_db['minutos_aviso_entregar_tarde']  # 3*60  # 3 horas

        tiempo_aviso_recoger = configuraciones_db['minutos_aviso_recoger']  # 6*60  # minutos, 6 horas
        tiempo_aviso_recoger_tarde = configuraciones_db['minutos_aviso_recoger_tarde']  # 3*60  # 3 horas

        tiempo_aviso_finalizar = configuraciones_db['minutos_aviso_finalizar']  # 3*60  # minutos, 3 horas
        tiempo_aviso_finalizar_tarde = configuraciones_db['minutos_aviso_finalizar_tarde']  # 6*60  # 6 horas

        # print('cargado....')
        # # para entregar
        # fecha_aviso_entrega = add_minutes_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd HH:ii:ss', minutos_add=0-tiempo_aviso_entrega)
        # fecha_aviso_entrega_tarde = add_minutes_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd HH:ii:ss', minutos_add=0-tiempo_aviso_entrega_tarde)

        # # para recoger
        # fecha_aviso_recoger = add_minutes_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd HH:ii:ss', minutos_add=0-tiempo_aviso_recoger)
        # fecha_aviso_recoger_tarde = add_minutes_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd HH:ii:ss', minutos_add=0-tiempo_aviso_recoger_tarde)

        # # para finalizar
        # fecha_aviso_finalizar = add_minutes_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd HH:ii:ss', minutos_add=tiempo_aviso_finalizar)
        # fecha_aviso_finalizar_tarde = add_minutes_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd HH:ii:ss', minutos_add=tiempo_aviso_finalizar_tarde)

        sql = "SELECT v.numero_contrato, v.apellidos, v.nombres, v.fecha_evento, v.fecha_entrega, v.fecha_devolucion, v.status_id "
        sql += f"FROM ventas v WHERE v.status_id IN ('{settings.STATUS_VENTA}', '{settings.STATUS_SALIDA_ALMACEN}', '{settings.STATUS_VUELTA_ALMACEN}') "
        sql += "ORDER BY v.fecha_evento, v.fecha_entrega "
        #print('sql: ', sql)

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                fecha_evento = row[3]
                numero_contrato = row[0]
                fecha_entrega = row[4]
                fecha_entrega_r1 = add_minutes_datetime(fecha_entrega, minutos_add=0-tiempo_aviso_entrega)
                fecha_entrega_r1_int = get_fecha_int(fecha_entrega_r1)
                fecha_entrega_r2 = add_minutes_datetime(fecha_entrega, minutos_add=0-tiempo_aviso_entrega_tarde)
                fecha_entrega_r2_int = get_fecha_int(fecha_entrega_r2)

                fecha_devolucion = row[5]
                fecha_devolucion_r1 = add_minutes_datetime(fecha_devolucion, minutos_add=0-tiempo_aviso_recoger)
                fecha_devolucion_r1_int = get_fecha_int(fecha_devolucion_r1)
                fecha_devolucion_r2 = add_minutes_datetime(fecha_devolucion, minutos_add=0-tiempo_aviso_recoger_tarde)
                fecha_devolucion_r2_int = get_fecha_int(fecha_devolucion_r2)
                status_venta = row[6]

                fecha_finalizar_r1 = add_minutes_datetime(fecha_devolucion, minutos_add=tiempo_aviso_finalizar)
                fecha_finalizar_r1_int = get_fecha_int(fecha_finalizar_r1)
                fecha_finalizar_r2 = add_minutes_datetime(fecha_devolucion, minutos_add=tiempo_aviso_finalizar_tarde)
                fecha_finalizar_r2_int = get_fecha_int(fecha_finalizar_r2)

                if status_venta == settings.STATUS_VENTA:
                    if fecha_actual_int >= fecha_entrega_r1_int and fecha_actual_int <= fecha_entrega_r2_int:
                        dato = {}
                        dato['tipo'] = 'E'
                        dato['tipo_notificacion'] = 'warning'
                        fecha = get_date_show(fecha=fecha_entrega, formato='dd-MMM-yyyy HH:ii', formato_ori='yyyy-mm-dd HH:ii:ss')
                        dato['descripcion'] = 'E - ' + fecha + ', &#35; ' + numero_contrato
                        dato['url'] = 'ventas'
                        lista_notificaciones.append(dato)
                        cantidad_warning += 1
                        cantidad += 1
                    elif fecha_actual_int > fecha_entrega_r2_int:
                        dato = {}
                        dato['tipo'] = 'E'
                        dato['tipo_notificacion'] = 'danger'
                        fecha = get_date_show(fecha=fecha_entrega, formato='dd-MMM-yyyy HH:ii', formato_ori='yyyy-mm-dd HH:ii:ss')
                        dato['descripcion'] = 'E - ' + fecha + ', &#35; ' + numero_contrato
                        dato['url'] = 'ventas'
                        lista_notificaciones.append(dato)
                        cantidad_danger += 1
                        cantidad += 1

                if status_venta == settings.STATUS_SALIDA_ALMACEN:
                    if fecha_actual_int >= fecha_devolucion_r1_int and fecha_actual_int <= fecha_devolucion_r2_int:
                        dato = {}
                        dato['tipo'] = 'R'
                        dato['tipo_notificacion'] = 'warning'
                        fecha = get_date_show(fecha=fecha_devolucion, formato='dd-MMM-yyyy HH:ii', formato_ori='yyyy-mm-dd HH:ii:ss')
                        dato['descripcion'] = 'R - ' + fecha + ', &#35; ' + numero_contrato
                        dato['url'] = 'ventas'
                        lista_notificaciones.append(dato)
                        cantidad_warning += 1
                        cantidad += 1

                    if fecha_actual_int > fecha_devolucion_r2_int:
                        dato = {}
                        dato['tipo'] = 'R'
                        dato['tipo_notificacion'] = 'danger'
                        fecha = get_date_show(fecha=fecha_devolucion, formato='dd-MMM-yyyy HH:ii', formato_ori='yyyy-mm-dd HH:ii:ss')
                        dato['descripcion'] = 'R - ' + fecha + ', &#35; ' + numero_contrato
                        dato['url'] = 'ventas'
                        lista_notificaciones.append(dato)
                        cantidad_danger += 1
                        cantidad += 1

                if status_venta == settings.STATUS_VUELTA_ALMACEN:
                    if fecha_actual_int >= fecha_finalizar_r1_int and fecha_actual_int <= fecha_finalizar_r2_int:
                        dato = {}
                        dato['tipo'] = 'F'
                        dato['tipo_notificacion'] = 'warning'
                        fecha = get_date_show(fecha=fecha_devolucion, formato='dd-MMM-yyyy HH:ii', formato_ori='yyyy-mm-dd HH:ii:ss')
                        dato['descripcion'] = 'F - ' + fecha + ', &#35; ' + numero_contrato
                        dato['url'] = 'ventas'
                        lista_notificaciones.append(dato)
                        cantidad_warning += 1
                        cantidad += 1

                    if fecha_actual_int > fecha_finalizar_r2_int:
                        dato = {}
                        dato['tipo'] = 'F'
                        dato['tipo_notificacion'] = 'danger'
                        fecha = get_date_show(fecha=fecha_devolucion, formato='dd-MMM-yyyy HH:ii', formato_ori='yyyy-mm-dd HH:ii:ss')
                        dato['descripcion'] = 'F - ' + fecha + ', &#35; ' + numero_contrato
                        dato['url'] = 'ventas'
                        lista_notificaciones.append(dato)
                        cantidad_danger += 1
                        cantidad += 1

        #print('lista notificaciones: ', lista_notificaciones)
        retorno['cantidad'] = cantidad
        retorno['cantidad_danger'] = cantidad_danger
        retorno['cantidad_warning'] = cantidad_warning
        retorno['lista_notificaciones'] = lista_notificaciones

        return retorno

    except Exception as e:
        retorno['cantidad'] = cantidad
        retorno['cantidad_danger'] = cantidad_danger
        retorno['cantidad_warning'] = cantidad_warning
        retorno['lista_notificaciones'] = lista_notificaciones

        return retorno
