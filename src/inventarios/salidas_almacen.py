import os
# from pages.views import lista_productos
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.apps import apps

# settings de la app
from django.conf import settings
# propios
from configuraciones.models import Almacenes
from inventarios.models import Registros, RegistrosDetalles

# para los usuarios
from utils.permissions import get_user_permission_operation, get_permissions_user, get_system_settings

# clases por modulo
from controllers.inventarios.SalidasAlmacenController import SalidasAlmacenController
from controllers.ListasController import ListasController
from controllers.productos.ProductosController import ProductosController

from controllers.inventarios.StockController import StockController

# reportes
import io
from django.http import FileResponse
from reportes.inventarios.rptSalidaAlmacen import rptSalidaAlmacen


salida_almacen_controller = SalidasAlmacenController()
lista_controller = ListasController()

# salidas almacen


@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_SALIDAS_ALMACEN, 'lista'), 'without_permission')
def salidas_almacen_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_SALIDAS_ALMACEN)
    stock_controller = StockController()

    vender_fracciones = 'no'

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'anular', 'print', 'stock_producto']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = salidas_almacen_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'anular':
            respuesta = salidas_almacen_nullify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'print':
            if permisos.imprimir:
                try:
                    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
                    registro = apps.get_model('inventarios', 'Registros').objects.get(pk=int(request.POST['id']))
                    if not salida_almacen_controller.permission_registro(user_perfil, registro):
                        return render(request, 'pages/without_permission.html', {})

                    buffer = io.BytesIO()
                    rptSalidaAlmacen(buffer, request.user, int(request.POST['id']))

                    buffer.seek(0)
                    return FileResponse(buffer, filename='salida_almacen_'+str(request.POST['id'])+'.pdf')

                except Exception as ex:
                    return render(request, 'pages/internal_error.html', {'error': str(ex)})

            else:
                return render(request, 'pages/without_permission.html', {})

        # stock del producto
        if operation == 'stock_producto':
            producto_id = request.POST['id'].strip()
            almacen_id = request.POST['almacen'].strip()

            stock_producto = stock_controller.stock_producto(producto_id=producto_id, user_perfil=request.user, almacen_id=almacen_id)
            # lista de ids
            stock_ids = ''
            for stock in stock_producto:
                stock_ids += str(stock.stock_id) + ','
            if len(stock_ids) > 0:
                stock_ids = stock_ids[0:len(stock_ids)-1]

            context_stock = {
                'stock_producto': stock_producto,
                'stock_ids': stock_ids,
                'producto_id': producto_id,
                'vender_fracciones': vender_fracciones,
                'autenticado': 'si',
                'stock_js': 'SA',
            }
            return render(request, 'inventarios/stock_producto_sin_fechas_lote.html', context_stock)

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    salidas_lista = salida_almacen_controller.index(request)
    salidas_session = request.session[salida_almacen_controller.modulo_session]

    # lista de almacenes
    #lista_almacenes = Almacenes.objects.select_related('sucursal_id').filter(status_id=salida_almacen_controller.status_activo).order_by('sucursal_id__sucursal', 'almacen')
    lista_almacenes = lista_controller.get_lista_almacenes(request.user, None)

    # print(zonas_session)
    context = {
        'salidas': salidas_lista,
        'session': salidas_session,
        'permisos': permisos,
        'lista_almacenes': lista_almacenes,
        'url_main': '',
        'estado_anulado': salida_almacen_controller.anulado,
        'autenticado': 'si',

        'js_file': salida_almacen_controller.modulo_session,
        'columnas': salida_almacen_controller.columnas,
        'module_x': settings.MOD_SALIDAS_ALMACEN,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'inventarios/salidas_almacen.html', context)


# salidas almacen add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_SALIDAS_ALMACEN, 'adicionar'), 'without_permission')
def salidas_almacen_add(request):

    producto_controller = ProductosController()
    # guardamos
    if 'add_x' in request.POST.keys():
        if salida_almacen_controller.save(request):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Salidas Almacen!', 'description': 'Se agrego la nueva salida'}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Salidas Almacen!', 'description': salida_almacen_controller.error_operation})

    # lista de productos
    #lista_productos = producto_controller.lista_productos(combos=1)
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
        'operation_x': 'add',
        'lista_productos': lista_productos,
        'lista_almacenes': lista_almacenes,
        'filas': filas,
        'db_tags': db_tags,
        'control_form': salida_almacen_controller.control_form,
        'js_file': salida_almacen_controller.modulo_session,
        'autenticado': 'si',

        'module_x': settings.MOD_SALIDAS_ALMACEN,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }

    return render(request, 'inventarios/salidas_almacen_form_sin_fechas_lote.html', context)


# salidas almacen anular
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_SALIDAS_ALMACEN, 'anular'), 'without_permission')
def salidas_almacen_nullify(request, registro_id):
    # url modulo
    registro_check = Registros.objects.filter(pk=registro_id)
    if not registro_check:
        return render(request, 'pages/without_permission.html', {})

    registro = Registros.objects.get(pk=registro_id)
    lista_controller = ListasController()

    if registro.status_id.status_id == salida_almacen_controller.anulado:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Salidas Almacen!', 'description': 'El registro ya esta anulado'}
        request.session.modified = True
        return False

    # verificamos tipo de movimiento
    if not registro.tipo_movimiento == 'SALIDA':
        return render(request, 'pages/without_permission.html', {})

    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
    if not salida_almacen_controller.permission_registro(user_perfil, registro):
        return render(request, 'pages/without_permission.html', {})

    # confirma eliminacion
    existe_error = False
    if 'anular_x' in request.POST.keys():
        if salida_almacen_controller.can_anular(registro_id, user_perfil) and salida_almacen_controller.anular(request, registro_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Salidas Almacen!', 'description': 'Se anulo el registro: '+request.POST['id']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Salidas Almacen!', 'description': salida_almacen_controller.error_operation})

    if salida_almacen_controller.can_anular(registro_id, user_perfil):
        puede_anular = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Salidas Almacen!', 'description': 'No puede anular este registro, ' + salida_almacen_controller.error_operation})
        puede_anular = 0

    # restricciones de columna
    db_tags = {}

    # lista de almacenes
    lista_almacenes = lista_controller.get_lista_almacenes(request.user, None)
    # detalles
    detalles = RegistrosDetalles.objects.filter(registro_id=registro).order_by('registro_detalle_id')

    context = {
        'url_main': '',
        'operation_x': 'anular',
        'registro': registro,
        'detalles': detalles,
        'lista_almacenes': lista_almacenes,
        'db_tags': db_tags,
        'control_form': salida_almacen_controller.control_form,
        'js_file': salida_almacen_controller.modulo_session,
        'puede_anular': puede_anular,
        'error_anular': salida_almacen_controller.error_operation,
        'autenticado': 'si',

        'module_x': settings.MOD_SALIDAS_ALMACEN,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'anular',
        'operation_x2': '',
        'operation_x3': '',

        'id': registro_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'inventarios/salidas_almacen_form_sin_fechas_lote.html', context)
