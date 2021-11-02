import os
from django.apps.registry import apps
# from pages.views import lista_productos
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

# settings de la app
from django.conf import settings
from inventarios.models import Registros, RegistrosDetalles

# para los usuarios
from utils.permissions import get_user_permission_operation, get_permissions_user, get_system_settings

# clases por modulo
from controllers.inventarios.IngresosAlmacenController import IngresosAlmacenController
from controllers.ListasController import ListasController
from controllers.productos.ProductosController import ProductosController

# reportes
import io
from django.http import FileResponse
from reportes.inventarios.rptIngresoAlmacen import rptIngresoAlmacen

ingreso_almacen_controller = IngresosAlmacenController()


# ingresos almacen
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_INGRESOS_ALMACEN, 'lista'), 'without_permission')
def ingresos_almacen_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_INGRESOS_ALMACEN)

    lista_controller = ListasController()

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'anular', 'print']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = ingresos_almacen_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'anular':
            respuesta = ingresos_almacen_nullify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'print':
            if permisos.imprimir:
                try:
                    # if not get_user_permission_operation(request.user, settings.MOD_INGRESOS_ALMACEN, 'imprimir', 'registro_id', int(request.POST['id'].strip()), 'inventarios', 'Registros'):
                    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
                    registro = apps.get_model('inventarios', 'Registros').objects.get(pk=int(request.POST['id']))
                    if not ingreso_almacen_controller.permission_registro(user_perfil, registro):
                        return render(request, 'pages/without_permission.html', {})

                    buffer = io.BytesIO()
                    rptIngresoAlmacen(buffer, request.user, int(request.POST['id']))

                    buffer.seek(0)
                    return FileResponse(buffer, filename='ingreso_almacen_'+str(request.POST['id'])+'.pdf')

                except Exception as ex:
                    return render(request, 'pages/internal_error.html', {'error': str(ex)})

            else:
                return render(request, 'pages/without_permission.html', {})

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    ingresos_lista = ingreso_almacen_controller.index(request)
    ingresos_session = request.session[ingreso_almacen_controller.modulo_session]

    # lista de almacenes
    lista_almacenes = lista_controller.get_lista_almacenes(request.user, None)

    # print(zonas_session)
    context = {
        'ingresos': ingresos_lista,
        'session': ingresos_session,
        'permisos': permisos,
        'lista_almacenes': lista_almacenes,
        'url_main': '',
        'estado_anulado': ingreso_almacen_controller.anulado,
        'autenticado': 'si',

        'js_file': ingreso_almacen_controller.modulo_session,
        'columnas': ingreso_almacen_controller.columnas,
        'module_x': settings.MOD_INGRESOS_ALMACEN,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'inventarios/ingresos_almacen.html', context)


# ingresos almacen add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_INGRESOS_ALMACEN, 'adicionar'), 'without_permission')
def ingresos_almacen_add(request):

    producto_controller = ProductosController()
    lista_controller = ListasController()
    system_settings = get_system_settings()
    vender_fracciones = 'no'

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if ingreso_almacen_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ingresos Almacen!', 'description': 'Se agrego el nuevo ingreso'}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ingresos Almacen!', 'description': ingreso_almacen_controller.error_operation})

    # lista de productos
    lista_productos = producto_controller.lista_productos()

    # restricciones de columna
    db_tags = {}

    # lista de almacenes
    lista_almacenes = lista_controller.get_lista_almacenes(request.user, None)

    # cantidad de filas
    filas = []
    for i in range(1, 51):
        filas.append(i)

    context = {
        'url_main': '',
        'lista_productos': lista_productos,
        'lista_almacenes': lista_almacenes,
        'filas': filas,
        'db_tags': db_tags,
        'control_form': ingreso_almacen_controller.control_form,
        'js_file': ingreso_almacen_controller.modulo_session,
        'vender_fracciones': vender_fracciones,

        'autenticado': 'si',

        'module_x': settings.MOD_INGRESOS_ALMACEN,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }

    return render(request, 'inventarios/ingresos_almacen_form_sin_fechas_lote.html', context)


# ingresos almacen anular
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_INGRESOS_ALMACEN, 'anular'), 'without_permission')
def ingresos_almacen_nullify(request, registro_id):
    # url modulo
    registro_check = Registros.objects.filter(pk=registro_id)
    if not registro_check:
        return render(request, 'pages/without_permission.html', {})

    registro = Registros.objects.get(pk=registro_id)
    lista_controller = ListasController()

    # verificamos el estado
    if registro.status_id.status_id == ingreso_almacen_controller.anulado:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ingresos Almacen!', 'description': 'El registro ya esta anulado'}
        request.session.modified = True
        return False

    # verificamos tipo de movimiento
    if not registro.tipo_movimiento == 'INGRESO':
        return render(request, 'pages/without_permission.html', {})

    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
    if not ingreso_almacen_controller.permission_registro(user_perfil, registro):
        return render(request, 'pages/without_permission.html', {})

    # confirma eliminacion
    if 'anular_x' in request.POST.keys():
        if ingreso_almacen_controller.can_anular(registro_id, user_perfil) and ingreso_almacen_controller.anular(request, registro_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ingresos Almacen!', 'description': 'Se anulo el registro: '+request.POST['id']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ingresos Almacen!', 'description': ingreso_almacen_controller.error_operation})

    if ingreso_almacen_controller.can_anular(registro_id, user_perfil):
        puede_anular = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ingresos Almacen!', 'description': 'No puede anular este registro, ' + ingreso_almacen_controller.error_operation})
        puede_anular = 0

    # restricciones de columna
    db_tags = {}

    # lista de almacenes
    lista_almacenes = lista_controller.get_lista_almacenes(request.user, None)
    # detalles
    detalles = RegistrosDetalles.objects.filter(registro_id=registro).order_by('registro_detalle_id')

    context = {
        'url_main': '',
        'registro': registro,
        'detalles': detalles,
        'lista_almacenes': lista_almacenes,
        'db_tags': db_tags,
        'control_form': ingreso_almacen_controller.control_form,
        'js_file': ingreso_almacen_controller.modulo_session,
        'puede_anular': puede_anular,
        'error_anular': ingreso_almacen_controller.error_operation,
        'autenticado': 'si',

        'module_x': settings.MOD_INGRESOS_ALMACEN,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'anular',
        'operation_x2': '',
        'operation_x3': '',

        'id': registro_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'inventarios/ingresos_almacen_form_sin_fechas_lote.html', context)
