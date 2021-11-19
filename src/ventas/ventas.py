from django.apps import apps
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

# settings de la app
from django.conf import settings
from ventas.models import Ventas, VentasAumentos, VentasAumentosDetalles, VentasDetalles
from utils.dates_functions import get_date_show, get_date_to_db, get_horas, get_minutos

# para los usuarios
from utils.permissions import current_date, get_user_permission_operation, get_permissions_user, get_system_settings

# clases por modulo
from controllers.ventas.VentasController import VentasController
from controllers.ListasController import ListasController
from controllers.productos.ProductosController import ProductosController
from controllers.SystemController import SystemController
from controllers.clientes.ClientesController import ClientesController
from controllers.cajas.CajasController import CajasController

# reportes
import io
from django.http import FileResponse

from reportes.ventas.rptVentasConCostos import rptVentasConCostos
from reportes.ventas.rptVentasSinCostos import rptVentasSinCostos
from reportes.ventas.rptVentasResumen import rptVentasResumen

from reportes.cajas.rptCajaEgresoRecibo import rptCajaEgresoRecibo
from reportes.cajas.rptCajaIngresoRecibo import rptCajaIngresoRecibo

venta_controller = VentasController()
lista_controller = ListasController()
producto_controller = ProductosController()
system_controller = SystemController()
cliente_controller = ClientesController()
caja_controller = CajasController()


# ventas
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'lista'), 'without_permission')
def ventas_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_VENTAS)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'modify', 'anular',
                             'buscar_cliente', 'stock_productos',
                             'pasar_venta', 'pasar_venta_anular',
                             'aumento_pedido',
                             'pasar_salida', 'pasar_salida_anular',
                             'pasar_vuelta', 'pasar_vuelta_anular',
                             'gastos', 'gastos_print', 'cobros', 'cobros_print',
                             'pasar_finalizado', 'pasar_finalizado_anular',
                             'imprimir_con_costos', 'imprimir_sin_costos',
                             'print_resumen']:
            return render(request, 'pages/without_permission.html', {})

        # buscar cliente
        if operation == 'buscar_cliente':
            datos_cliente = cliente_controller.buscar_cliente(ci_nit=request.POST['ci_nit'], apellidos=request.POST['apellidos'], nombres=request.POST['nombres'])
            # print(datos_cliente)
            context_buscar = {
                'clientes': datos_cliente,
                'autenticado': 'si',
            }
            return render(request, 'ventas/clientes_buscar.html', context_buscar)

        # stock producto
        if operation == 'stock_productos':
            try:
                fecha_entrega = request.POST['fecha_entrega'].strip()
                hora_entrega = request.POST['hora_entrega'].strip()
                minuto_entrega = request.POST['minuto_entrega'].strip()
                fecha_devolucion = request.POST['fecha_devolucion'].strip()
                hora_devolucion = request.POST['hora_devolucion'].strip()
                minuto_devolucion = request.POST['minuto_devolucion'].strip()

                fecha_ini = get_date_to_db(fecha=fecha_entrega, formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo=hora_entrega + ':' + minuto_entrega + ':00')
                fecha_fin = get_date_to_db(fecha=fecha_devolucion, formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo=hora_devolucion + ':' + minuto_devolucion + ':00')
                #print('fecha ini: ', fecha_ini, ' fecha fin: ', fecha_fin)
                datos_productos = venta_controller.stock_productos(fecha_ini, fecha_fin)
                #print('datos productos...: ', datos_productos)
                context_buscar = {
                    'datos_productos': datos_productos,
                    'autenticado': 'si',
                }
                return render(request, 'ventas/stock_productos.html', context_buscar)

            except Exception as ex:
                return render(request, 'pages/internal_error.html', {'error': str(ex)})

        if operation == 'add':
            respuesta = ventas_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = ventas_modificar_preventa(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'pasar_venta':
            respuesta = ventas_pasar_venta(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'pasar_venta_anular':
            respuesta = ventas_pasar_venta_anular(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'anular':
            respuesta = ventas_nullify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'aumento_pedido':
            respuesta = aumento_pedido(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'pasar_salida':
            respuesta = ventas_pasar_salida(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'pasar_salida_anular':
            respuesta = ventas_pasar_salida_anular(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'pasar_vuelta':
            respuesta = ventas_pasar_vuelta(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'pasar_vuelta_anular':
            respuesta = ventas_pasar_vuelta_anular(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'gastos':
            respuesta = ventas_gastos(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'cobros':
            respuesta = ventas_cobros(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'pasar_finalizado':
            respuesta = ventas_pasar_finalizado(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'pasar_finalizado_anular':
            respuesta = ventas_pasar_finalizado_anular(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'imprimir_con_costos':
            if permisos.imprimir:
                try:
                    buffer = io.BytesIO()
                    rptVentasConCostos(buffer, request.user, int(request.POST['id']))

                    buffer.seek(0)
                    return FileResponse(buffer, filename='venta_'+str(request.POST['id'])+'.pdf')

                except Exception as ex:
                    return render(request, 'pages/internal_error.html', {'error': str(ex)})

            else:
                return render(request, 'pages/without_permission.html', {})

        if operation == 'imprimir_sin_costos':
            if permisos.imprimir:
                try:
                    buffer = io.BytesIO()
                    rptVentasSinCostos(buffer, request.user, int(request.POST['id']))

                    buffer.seek(0)
                    return FileResponse(buffer, filename='venta_'+str(request.POST['id'])+'.pdf')

                except Exception as ex:
                    return render(request, 'pages/internal_error.html', {'error': str(ex)})

            else:
                return render(request, 'pages/without_permission.html', {})

        if operation == 'gastos_print':
            if permisos.imprimir:
                try:
                    buffer = io.BytesIO()
                    rptCajaEgresoRecibo(buffer, int(request.POST['id']))

                    buffer.seek(0)
                    return FileResponse(buffer, filename='ce_venta_recibo.pdf')

                except Exception as ex:
                    return render(request, 'pages/internal_error.html', {'error': str(ex)})

            else:
                return render(request, 'pages/without_permission.html', {})

        if operation == 'cobros_print':
            if permisos.imprimir:
                try:
                    buffer = io.BytesIO()
                    rptCajaIngresoRecibo(buffer, int(request.POST['id']))

                    buffer.seek(0)
                    return FileResponse(buffer, filename='ci_venta_recibo.pdf')

                except Exception as ex:
                    return render(request, 'pages/internal_error.html', {'error': str(ex)})

            else:
                return render(request, 'pages/without_permission.html', {})

        if operation == 'print_resumen':
            if permisos.imprimir:
                try:
                    buffer = io.BytesIO()
                    rptVentasResumen(buffer, request.user, int(request.POST['id']))

                    buffer.seek(0)
                    return FileResponse(buffer, filename='venta_resumen.pdf')

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
    ventas_lista = venta_controller.index(request)
    ventas_session = request.session[venta_controller.modulo_session]

    # lista de almacenes
    lista_almacenes = lista_controller.get_lista_almacenes(request.user, None, settings.MOD_VENTAS)

    # print(zonas_session)
    context = {
        'ventas': ventas_lista,
        'session': ventas_session,
        'permisos': permisos,
        'lista_almacenes': lista_almacenes,
        'url_main': '',
        'estado_anulado': venta_controller.anulado,
        'estado_preventa': venta_controller.preventa,
        'estado_venta': venta_controller.venta,
        'estado_salida': venta_controller.salida_almacen,
        'estado_vuelta': venta_controller.vuelta_almacen,
        'estado_finalizado': venta_controller.finalizado,
        'autenticado': 'si',

        'js_file': venta_controller.modulo_session,
        'columnas': venta_controller.columnas,
        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'ventas/ventas.html', context)


# ventas add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'adicionar'), 'without_permission')
def ventas_add(request):

    vender_fracciones = 'no'

    # guardamos
    if 'add_x' in request.POST.keys():
        if venta_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se agrego la nueva preventa'}
            request.session.modified = True
            return True
        else:
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    # lista de productos
    lista_productos = producto_controller.lista_productos()
    # lista de almacenes
    lista_almacenes = lista_controller.get_lista_almacenes(request.user, None, settings.MOD_VENTAS)

    # cantidad de filas
    filas = []
    for i in range(1, 51):
        filas.append(i)

    fecha_actual = get_date_show(fecha=current_date(), formato_ori='yyyy-mm-dd', formato="dd-MMM-yyyy")
    fecha_evento = fecha_actual
    fecha_entrega = fecha_actual
    fecha_devolucion = fecha_actual
    horas = system_controller.get_horas()
    minutos = system_controller.get_minutos()

    context = {
        'url_main': '',
        'lista_productos': lista_productos,
        'lista_almacenes': lista_almacenes,
        'filas': filas,
        'fecha_evento': fecha_evento,
        'fecha_entrega': fecha_entrega,
        'fecha_devolucion': fecha_devolucion,
        'horas': horas,
        'minutos': minutos,

        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'vender_fracciones': vender_fracciones,

        'autenticado': 'si',

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation': venta_controller.preventa,
        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/ventas_preventa.html', context)


# ventas modify
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'modificar'), 'without_permission')
def ventas_modificar_preventa(request, venta_id):

    vender_fracciones = 'no'
    venta_check = apps.get_model('ventas', 'Ventas').objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = venta_check.first()
    if venta.status_id != venta_controller.status_preventa:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    if 'modify_x' in request.POST.keys():
        if venta_controller.save(request, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se modifico la preventa'}
            request.session.modified = True
            return True
        else:
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    # lista de productos
    lista_productos = producto_controller.lista_productos()
    # lista de almacenes
    lista_almacenes = lista_controller.get_lista_almacenes(request.user, None, settings.MOD_VENTAS)

    # detalles
    venta_detalles = apps.get_model('ventas', 'VentasDetalles').objects.filter(venta_id=venta)
    len_detalles = len(venta_detalles)

    datos_productos = venta_controller.stock_productos(venta.fecha_entrega, venta.fecha_devolucion)

    # cantidad de filas
    filas = []
    for i in range(1, 51):
        filas.append(i)

    fecha_evento = get_date_show(fecha=venta.fecha_evento)
    fecha_entrega = get_date_show(fecha=venta.fecha_entrega)
    hora_entrega = get_horas(fecha=venta.fecha_entrega)
    minuto_entrega = get_minutos(fecha=venta.fecha_entrega)
    fecha_devolucion = get_date_show(fecha=venta.fecha_devolucion)
    hora_devolucion = get_horas(fecha=venta.fecha_devolucion)
    minuto_devolucion = get_minutos(fecha=venta.fecha_devolucion)

    horas = system_controller.get_horas()
    minutos = system_controller.get_minutos()

    context = {
        'url_main': '',
        'lista_productos': lista_productos,
        'lista_almacenes': lista_almacenes,
        'filas': filas,
        'fecha_evento': fecha_evento,
        'fecha_entrega': fecha_entrega,
        'hora_entrega': hora_entrega,
        'minuto_entrega': minuto_entrega,
        'fecha_devolucion': fecha_devolucion,
        'hora_devolucion': hora_devolucion,
        'minuto_devolucion': minuto_devolucion,
        'datos_productos': datos_productos,

        'horas': horas,
        'minutos': minutos,
        'venta': venta,
        'venta_detalles': venta_detalles,
        'len_detalles': len_detalles,
        'len_mostrar': len_detalles + 2,

        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'vender_fracciones': vender_fracciones,

        'autenticado': 'si',

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation': venta_controller.preventa,
        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/ventas_preventa.html', context)


# ventas anular
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'anular'), 'without_permission')
def ventas_nullify(request, venta_id):
    # url modulo
    venta_check = Ventas.objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = Ventas.objects.get(pk=venta_id)

    # verificamos el estado
    if venta.status_id.status_id == venta_controller.anulado:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'El registro ya esta anulado'}
        request.session.modified = True
        return False

    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
    if not venta_controller.permission_operation(user_perfil, 'anular'):
        return render(request, 'pages/without_permission.html', {})

    # confirma eliminacion
    if 'anular_x' in request.POST.keys():
        if venta_controller.can_anular(venta_id, user_perfil) and venta_controller.anular(request, venta_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se anulo el registro: '+request.POST['id']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    if venta_controller.can_anular(venta_id, user_perfil):
        puede_anular = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': 'No puede anular este registro, ' + venta_controller.error_operation})
        puede_anular = 0

    # restricciones de columna
    db_tags = {}

    # detalles
    venta_detalles = VentasDetalles.objects.filter(venta_id=venta).order_by('venta_detalle_id')

    fecha_evento = get_date_show(fecha=venta.fecha_evento)
    fecha_entrega = get_date_show(fecha=venta.fecha_entrega)
    hora_entrega = get_horas(fecha=venta.fecha_entrega)
    minuto_entrega = get_minutos(fecha=venta.fecha_entrega)
    fecha_devolucion = get_date_show(fecha=venta.fecha_devolucion)
    hora_devolucion = get_horas(fecha=venta.fecha_devolucion)
    minuto_devolucion = get_minutos(fecha=venta.fecha_devolucion)

    horas = system_controller.get_horas()
    minutos = system_controller.get_minutos()

    context = {
        'url_main': '',
        'venta': venta,
        'venta_detalles': venta_detalles,
        'db_tags': db_tags,
        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'puede_anular': puede_anular,
        'error_anular': venta_controller.error_operation,
        'autenticado': 'si',

        'fecha_evento': fecha_evento,
        'fecha_entrega': fecha_entrega,
        'hora_entrega': hora_entrega,
        'minuto_entrega': minuto_entrega,
        'fecha_devolucion': fecha_devolucion,
        'hora_devolucion': hora_devolucion,
        'minuto_devolucion': minuto_devolucion,

        'horas': horas,
        'minutos': minutos,

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'anular',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    context['operation'] = venta_controller.preventa
    return render(request, 'ventas/ventas_preventa.html', context)


# ventas pasar venta
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'modificar'), 'without_permission')
def ventas_pasar_venta(request, venta_id):

    vender_fracciones = 'no'
    venta_check = apps.get_model('ventas', 'Ventas').objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = venta_check.first()
    if venta.status_id != venta_controller.status_preventa:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    if 'pasar_venta_x' in request.POST.keys():
        if venta_controller.save(request, type='pasar_venta'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se confirmo la venta'}
            request.session.modified = True
            return True
        else:
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    # detalles
    venta_detalles = apps.get_model('ventas', 'VentasDetalles').objects.filter(venta_id=venta)

    fecha_evento = get_date_show(fecha=venta.fecha_evento)
    fecha_entrega = get_date_show(fecha=venta.fecha_entrega)
    hora_entrega = get_horas(fecha=venta.fecha_entrega)
    minuto_entrega = get_minutos(fecha=venta.fecha_entrega)
    fecha_devolucion = get_date_show(fecha=venta.fecha_devolucion)
    hora_devolucion = get_horas(fecha=venta.fecha_devolucion)
    minuto_devolucion = get_minutos(fecha=venta.fecha_devolucion)

    horas = system_controller.get_horas()
    minutos = system_controller.get_minutos()

    datos_productos = venta_controller.stock_productos(venta.fecha_entrega, venta.fecha_devolucion)
    puede_confirmar = 1
    for detalle in venta_detalles:
        p_id = detalle.producto_id.producto_id
        if datos_productos[p_id] < 0:
            puede_confirmar = 0
            break

    context = {
        'url_main': '',
        'fecha_evento': fecha_evento,
        'fecha_entrega': fecha_entrega,
        'hora_entrega': hora_entrega,
        'minuto_entrega': minuto_entrega,
        'fecha_devolucion': fecha_devolucion,
        'hora_devolucion': hora_devolucion,
        'minuto_devolucion': minuto_devolucion,
        'datos_productos': datos_productos,
        'puede_confirmar': puede_confirmar,

        'horas': horas,
        'minutos': minutos,
        'venta': venta,
        'venta_detalles': venta_detalles,

        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'vender_fracciones': vender_fracciones,

        'autenticado': 'si',

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation': venta_controller.venta,
        'operation_x': 'pasar_venta',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/ventas_venta.html', context)


# pasar venta anular
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'anular'), 'without_permission')
def ventas_pasar_venta_anular(request, venta_id):
    # url modulo
    venta_check = Ventas.objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = Ventas.objects.get(pk=venta_id)

    # verificamos el estado
    if venta.status_id.status_id != venta_controller.venta:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'El registro no es una venta confirmada'}
        request.session.modified = True
        return False

    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
    if not venta_controller.permission_operation(user_perfil, 'anular'):
        return render(request, 'pages/without_permission.html', {})

    # confirma anulacion
    if 'anular_x' in request.POST.keys():
        if venta_controller.can_anular(venta_id, user_perfil) and venta_controller.anular(request, venta_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se anulo la venta: '+request.POST['id']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    if venta_controller.can_anular(venta_id, user_perfil):
        puede_anular = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': 'No puede anular este registro, ' + venta_controller.error_operation})
        puede_anular = 0

    # restricciones de columna
    db_tags = {}

    # detalles
    venta_detalles = VentasDetalles.objects.filter(venta_id=venta).order_by('venta_detalle_id')

    fecha_evento = get_date_show(fecha=venta.fecha_evento)
    fecha_entrega = get_date_show(fecha=venta.fecha_entrega)
    hora_entrega = get_horas(fecha=venta.fecha_entrega)
    minuto_entrega = get_minutos(fecha=venta.fecha_entrega)
    fecha_devolucion = get_date_show(fecha=venta.fecha_devolucion)
    hora_devolucion = get_horas(fecha=venta.fecha_devolucion)
    minuto_devolucion = get_minutos(fecha=venta.fecha_devolucion)

    horas = system_controller.get_horas()
    minutos = system_controller.get_minutos()

    context = {
        'url_main': '',
        'venta': venta,
        'venta_detalles': venta_detalles,
        'db_tags': db_tags,
        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'puede_anular': puede_anular,
        'error_anular': venta_controller.error_operation,
        'autenticado': 'si',

        'fecha_evento': fecha_evento,
        'fecha_entrega': fecha_entrega,
        'hora_entrega': hora_entrega,
        'minuto_entrega': minuto_entrega,
        'fecha_devolucion': fecha_devolucion,
        'hora_devolucion': hora_devolucion,
        'minuto_devolucion': minuto_devolucion,

        'horas': horas,
        'minutos': minutos,

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'pasar_venta_anular',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    context['operation'] = venta_controller.venta
    return render(request, 'ventas/ventas_venta.html', context)


# aumento pedido
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'modificar'), 'without_permission')
def aumento_pedido(request, venta_id):

    vender_fracciones = 'no'
    venta_check = Ventas.objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = Ventas.objects.get(pk=venta_id)

    # verificamos el estado
    if venta.status_id.status_id not in [venta_controller.venta, venta_controller.salida_almacen]:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'La venta tiene que estar en estado "venta" o "salida" '}
        request.session.modified = True
        return False

    # guardamos
    if 'aumento_pedido_x' in request.POST.keys():
        if venta_controller.save(request, type='aumento_pedido'):
            # request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se agrego el aumento'}
            # request.session.modified = True
            # return True
            messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Ventas Aumentos!', 'description': 'se registro el aumento correctamente'})
        else:
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    # anulamos
    if 'operation_x2' in request.POST.keys():
        operation2 = request.POST['operation_x2']
        if operation2 == 'aumento_pedido_anular_x':
            if venta_controller.anular_aumento(request, request.POST['vaid']):
                messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Ventas Aumentos!', 'description': 'se anulo el aumento correctamente'})
            else:
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    # lista de productos
    lista_productos = producto_controller.lista_productos()

    datos_productos = venta_controller.stock_productos(venta.fecha_entrega, venta.fecha_devolucion, ventas_not_in=str(venta.venta_id))

    # cantidad de filas
    filas = []
    for i in range(1, 51):
        filas.append(i)

    fecha_actual = get_date_show(fecha=current_date(), formato_ori='yyyy-mm-dd', formato="dd-MMM-yyyy")
    fecha_evento = fecha_actual
    fecha_entrega = fecha_actual
    fecha_devolucion = fecha_actual
    horas = system_controller.get_horas()
    minutos = system_controller.get_minutos()

    # lista de aumentos existentes
    lista_aumentos = VentasAumentos.objects.filter(venta_id=venta).order_by('created_at')

    context = {
        'url_main': '',
        'lista_productos': lista_productos,
        'datos_productos': datos_productos,
        'filas': filas,
        'fecha_evento': fecha_evento,
        'fecha_entrega': fecha_entrega,
        'fecha_devolucion': fecha_devolucion,
        'horas': horas,
        'minutos': minutos,
        'venta': venta,
        'lista_aumentos': lista_aumentos,
        'estado_anulado': venta_controller.anulado,

        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'vender_fracciones': vender_fracciones,

        'autenticado': 'si',

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation': 'aumento_pedido',
        'operation_x': 'aumento_pedido',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/aumento.html', context)


# ventas pasar salida
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'modificar'), 'without_permission')
def ventas_pasar_salida(request, venta_id):

    vender_fracciones = 'no'
    venta_check = apps.get_model('ventas', 'Ventas').objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = venta_check.first()
    if venta.status_id != venta_controller.status_venta:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    if 'pasar_salida_x' in request.POST.keys():
        if venta_controller.save(request, type='pasar_salida'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se realizo la salida de almacen'}
            request.session.modified = True
            return True
        else:
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    # detalles
    venta_detalles = apps.get_model('ventas', 'VentasDetalles').objects.filter(venta_id=venta)

    # aumentos
    lista_aumentos = VentasAumentos.objects.filter(venta_id=venta, status_id=venta_controller.status_venta).order_by('created_at')

    context = {
        'url_main': '',
        'venta': venta,
        'venta_detalles': venta_detalles,
        'lista_aumentos': lista_aumentos,

        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'vender_fracciones': vender_fracciones,

        'autenticado': 'si',

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation': venta_controller.salida_almacen,
        'operation_x': 'pasar_salida',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/ventas_salida.html', context)


# pasar salida anular
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'anular'), 'without_permission')
def ventas_pasar_salida_anular(request, venta_id):
    # url modulo
    venta_check = Ventas.objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = Ventas.objects.get(pk=venta_id)

    # verificamos el estado
    if venta.status_id.status_id != venta_controller.salida_almacen:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'El registro no es una salida de almacen'}
        request.session.modified = True
        return False

    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
    if not venta_controller.permission_operation(user_perfil, 'anular'):
        return render(request, 'pages/without_permission.html', {})

    # confirma anulacion
    if 'anular_x' in request.POST.keys():
        if venta_controller.can_anular(venta_id, user_perfil) and venta_controller.anular(request, venta_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se anulo la venta: '+request.POST['id']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    if venta_controller.can_anular(venta_id, user_perfil):
        puede_anular = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': 'No puede anular este registro, ' + venta_controller.error_operation})
        puede_anular = 0

    # restricciones de columna
    db_tags = {}

    # detalles
    venta_detalles = VentasDetalles.objects.filter(venta_id=venta).order_by('venta_detalle_id')

    # aumentos
    lista_aumentos = VentasAumentos.objects.filter(venta_id=venta, status_id=venta_controller.status_salida_almacen).order_by('created_at')

    context = {
        'url_main': '',
        'venta': venta,
        'venta_detalles': venta_detalles,
        'lista_aumentos': lista_aumentos,
        'db_tags': db_tags,
        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'puede_anular': puede_anular,
        'error_anular': venta_controller.error_operation,
        'autenticado': 'si',

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'pasar_salida_anular',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    context['operation'] = venta_controller.salida_almacen
    return render(request, 'ventas/ventas_salida.html', context)


# ventas pasar vuelta
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'modificar'), 'without_permission')
def ventas_pasar_vuelta(request, venta_id):

    vender_fracciones = 'no'
    venta_check = apps.get_model('ventas', 'Ventas').objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = venta_check.first()
    if venta.status_id != venta_controller.status_salida_almacen:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    if 'pasar_vuelta_x' in request.POST.keys():
        if venta_controller.save(request, type='pasar_vuelta'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se realizo la vuelta a almacen'}
            request.session.modified = True
            return True
        else:
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    # detalles
    lista_productos = []
    venta_detalles = apps.get_model('ventas', 'VentasDetalles').objects.filter(venta_id=venta).order_by('venta_detalle_id')
    for venta_d in venta_detalles:
        dato = {}
        dato['producto_id'] = venta_d.producto_id.producto_id
        dato['producto'] = venta_d.producto_id.linea_id.linea + ' - ' + venta_d.producto_id.producto
        dato['cantidad_salida'] = venta_d.cantidad_salida
        dato['costo_rotura'] = venta_d.producto_id.costo_rotura
        lista_productos.append(dato)

    # aumentos
    lista_aumentos = VentasAumentos.objects.filter(venta_id=venta, status_id=venta_controller.status_salida_almacen).order_by('created_at')
    for aumento in lista_aumentos:
        va_detalles = VentasAumentosDetalles.objects.filter(venta_aumento_id=aumento).order_by('venta_aumento_detalle_id')
        for detalle in va_detalles:
            # leemos los productos existentes
            pos = -1
            i = 0
            for producto in lista_productos:
                if producto['producto_id'] == detalle.producto_id.producto_id:
                    pos = i
                    break
                i = i+1

            if pos >= 0:
                lista_productos[pos]['cantidad_salida'] = lista_productos[pos]['cantidad_salida'] + detalle.cantidad_salida
            else:
                # aniadimos nuevo producto
                dato = {}
                dato['producto_id'] = detalle.producto_id.producto_id
                dato['producto'] = detalle.producto_id.linea_id.linea + ' - ' + detalle.producto_id.producto
                dato['cantidad_salida'] = detalle.cantidad_salida
                dato['costo_rotura'] = detalle.producto_id.costo_rotura
                lista_productos.append(dato)

    cant_productos = len(lista_productos)
    #print('cant productos...', cant_productos)

    context = {
        'url_main': '',
        'venta': venta,
        'venta_detalles': venta_detalles,
        'lista_aumentos': lista_aumentos,
        'lista_productos': lista_productos,
        'cant_productos': cant_productos,

        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'vender_fracciones': vender_fracciones,

        'autenticado': 'si',

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation': venta_controller.vuelta_almacen,
        'operation_x': 'pasar_vuelta',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/ventas_vuelta.html', context)


# pasar vuelta anular
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'anular'), 'without_permission')
def ventas_pasar_vuelta_anular(request, venta_id):
    # url modulo
    venta_check = Ventas.objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = Ventas.objects.get(pk=venta_id)

    # verificamos el estado
    if venta.status_id.status_id != venta_controller.vuelta_almacen:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'El registro no es una vuelta a almacen'}
        request.session.modified = True
        return False

    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
    if not venta_controller.permission_operation(user_perfil, 'anular'):
        return render(request, 'pages/without_permission.html', {})

    # confirma anulacion
    if 'anular_x' in request.POST.keys():
        if venta_controller.can_anular(venta_id, user_perfil) and venta_controller.anular(request, venta_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se anulo la venta: '+request.POST['id']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    if venta_controller.can_anular(venta_id, user_perfil):
        puede_anular = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': 'No puede anular este registro, ' + venta_controller.error_operation})
        puede_anular = 0

    # detalles
    lista_productos = []
    venta_detalles = apps.get_model('ventas', 'VentasDetalles').objects.filter(venta_id=venta).order_by('venta_detalle_id')
    for venta_d in venta_detalles:
        dato = {}
        dato['producto_id'] = venta_d.producto_id.producto_id
        dato['producto'] = venta_d.producto_id.linea_id.linea + ' - ' + venta_d.producto_id.producto
        dato['cantidad_salida'] = venta_d.cantidad_salida
        dato['cantidad_vuelta'] = venta_d.cantidad_vuelta
        if venta_d.costo_total_rotura > 0:
            dato['costo_rotura'] = venta_d.costo_total_rotura
        else:
            dato['costo_rotura'] = venta_d.producto_id.costo_rotura
        dato['refaccion'] = venta_d.costo_refaccion
        lista_productos.append(dato)

    # aumentos
    lista_aumentos = VentasAumentos.objects.filter(venta_id=venta, status_id=venta_controller.status_vuelta_almacen).order_by('created_at')
    for aumento in lista_aumentos:
        va_detalles = VentasAumentosDetalles.objects.filter(venta_aumento_id=aumento).order_by('venta_aumento_detalle_id')
        for detalle in va_detalles:
            # leemos los productos existentes
            pos = -1
            i = 0
            for producto in lista_productos:
                if producto['producto_id'] == detalle.producto_id.producto_id:
                    pos = i
                    break
                i = i+1

            if pos >= 0:
                lista_productos[pos]['cantidad_salida'] = lista_productos[pos]['cantidad_salida'] + detalle.cantidad_salida
            else:
                # aniadimos nuevo producto
                dato = {}
                dato['producto_id'] = detalle.producto_id.producto_id
                dato['producto'] = detalle.producto_id.linea_id.linea + ' - ' + detalle.producto_id.producto
                dato['cantidad_salida'] = detalle.cantidad_salida
                dato['cantidad_vuelta'] = detalle.cantidad_vuelta

                if detalle.costo_total_rotura > 0:
                    dato['costo_rotura'] = detalle.costo_total_rotura
                else:
                    dato['costo_rotura'] = detalle.producto_id.costo_rotura
                dato['refaccion'] = detalle.costo_refaccion

                lista_productos.append(dato)

    cant_productos = len(lista_productos)

    context = {
        'url_main': '',
        'venta': venta,
        'venta_detalles': venta_detalles,
        'lista_aumentos': lista_aumentos,
        'lista_productos': lista_productos,
        'cant_productos': cant_productos,
        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'puede_anular': puede_anular,
        'error_anular': venta_controller.error_operation,
        'autenticado': 'si',

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'pasar_vuelta_anular',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    context['operation'] = venta_controller.vuelta_almacen
    return render(request, 'ventas/ventas_vuelta.html', context)


# gastos sobre la venta
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'modificar'), 'without_permission')
def ventas_gastos(request, venta_id):
    # url modulo
    venta_check = Ventas.objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = Ventas.objects.get(pk=venta_id)

    # verificamos el estado
    if venta.status_id.status_id not in [venta_controller.venta, venta_controller.salida_almacen, venta_controller.vuelta_almacen]:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'El registro debe estar activo'}
        request.session.modified = True
        return False

    caja_lista = caja_controller.cash_active(current_date(), request.user, formato_ori='yyyy-mm-dd')

    if not caja_lista:
        # no tiene caja activa
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'Debe tener una caja activa'}
        request.session.modified = True
        return False

    caja_usuario = caja_lista[0]

    # confirma adicion gasto
    if 'gastos_x' in request.POST.keys():
        if venta_controller.add_gasto(venta_id, caja_usuario, request):
            # request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se adiciono el gasto correctamente'}
            # request.session.modified = True
            # return True
            messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Gastos!', 'description': 'se adiciono el gasto correctamente'})
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    # confirma anulacion gasto
    if 'operation_x2' in request.POST.keys():
        operation2 = request.POST['operation_x2']
        if operation2 == 'gastos_anular_x':
            user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
            if not venta_controller.permission_operation(user_perfil, 'anular'):
                return render(request, 'pages/without_permission.html', {})

            if venta_controller.anular_gasto(venta_id, caja_usuario, request):
                messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Gastos!', 'description': 'se anulo el gasto correctamente'})
            else:
                # error al modificar
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    # lista de gastos
    saldo_dia = caja_controller.day_balance(fecha=current_date(), Cajas=caja_usuario, formato_ori='yyyy-mm-dd')
    saldo_caja = saldo_dia[caja_usuario.caja_id]

    lista_gastos = apps.get_model('cajas', 'CajasEgresos').objects.filter(venta_id=venta.venta_id).order_by('caja_egreso_id')
    fecha_actual = get_date_show(fecha=current_date(), formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')

    context = {
        'url_main': '',
        'venta': venta,
        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'error_anular': venta_controller.error_operation,
        'autenticado': 'si',
        'lista_gastos': lista_gastos,
        'estado_anulado': venta_controller.anulado,
        'caja_usuario': caja_usuario,
        'saldo_caja': saldo_caja,
        'fecha_actual': fecha_actual,

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'gastos',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/ventas_gastos.html', context)


# cobros sobre la venta
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'modificar'), 'without_permission')
def ventas_cobros(request, venta_id):
    # url modulo
    venta_check = Ventas.objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = Ventas.objects.get(pk=venta_id)

    # verificamos el estado
    if venta.status_id.status_id not in [venta_controller.venta, venta_controller.salida_almacen, venta_controller.vuelta_almacen]:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'El registro debe estar activo'}
        request.session.modified = True
        return False

    caja_lista = caja_controller.cash_active(current_date(), request.user, formato_ori='yyyy-mm-dd')

    if not caja_lista:
        # no tiene caja activa
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'Debe tener una caja activa'}
        request.session.modified = True
        return False

    caja_usuario = caja_lista[0]

    # confirma adicion gasto
    if 'cobros_x' in request.POST.keys():
        if venta_controller.add_cobro(venta_id, caja_usuario, request):
            messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Cobros!', 'description': 'se adiciono el cobro correctamente'})
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cobros!', 'description': venta_controller.error_operation})

    # confirma anulacion gasto
    if 'operation_x2' in request.POST.keys():
        operation2 = request.POST['operation_x2']
        if operation2 == 'cobros_anular_x':
            user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
            if not venta_controller.permission_operation(user_perfil, 'anular'):
                return render(request, 'pages/without_permission.html', {})

            if venta_controller.anular_cobro(venta_id, caja_usuario, request):
                messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Gastos!', 'description': 'se anulo el cobro correctamente'})
            else:
                # error al modificar
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    saldo_inicial = venta.total
    venta_y_garantia = venta.total + venta.garantia_bs
    saldo_venta = saldo_inicial

    saldo_mas_gastos = saldo_inicial + venta.garantia_bs
    saldo_venta = saldo_venta + venta.garantia_bs

    # lista de gastos
    lista_gastos = apps.get_model('cajas', 'CajasEgresos').objects.filter(venta_id=venta.venta_id).order_by('caja_egreso_id')
    fecha_actual = get_date_show(fecha=current_date(), formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')
    # lista de ingresos
    lista_ingresos = apps.get_model('cajas', 'CajasIngresos').objects.filter(venta_id=venta.venta_id).order_by('caja_ingreso_id')

    # lista de aumentos
    #lista_aumentos = apps.get_model('ventas', 'VentasAumentos').objects.filter(venta_id=venta, status_id=venta_controller.status_activo).order_by('venta_aumento_id')

    total_gastos = 0
    for gasto in lista_gastos:
        if gasto.status_id == venta_controller.status_activo:
            saldo_venta = saldo_venta + gasto.monto
            saldo_mas_gastos = saldo_mas_gastos + gasto.monto
            total_gastos += gasto.monto

    total_cobros = 0
    for ingreso in lista_ingresos:
        if ingreso.status_id == venta_controller.status_activo:
            saldo_venta = saldo_venta - ingreso.monto
            total_cobros += ingreso.monto

    # total_aumentos = 0
    # for venta_aumento in lista_aumentos:
    #     saldo_venta += venta_aumento.total
    #     total_aumentos += venta_aumento.total

    # devolucion de productos y aumentos
    ventas_detalles = VentasDetalles.objects.filter(venta_id=venta)
    deuda_detalles = 0
    for detalle in ventas_detalles:
        deuda_detalles += detalle.total_vuelta_rotura

    #print('deuda detalles 1..: ', deuda_detalles)

    # aumentos
    filtro_aumento = {}
    filtro_aumento['venta_id'] = venta
    filtro_aumento['status_id__in'] = [venta_controller.status_venta, venta_controller.status_salida_almacen, venta_controller.status_vuelta_almacen]
    ventas_aumentos = VentasAumentos.objects.filter(**filtro_aumento)
    total_aumentos = 0
    for ve_aumento in ventas_aumentos:
        saldo_venta += ve_aumento.total
        total_aumentos += ve_aumento.total

        ventas_aumentos_detalles = VentasAumentosDetalles.objects.filter(venta_aumento_id=ve_aumento)
        for detalle in ventas_aumentos_detalles:
            deuda_detalles += detalle.total_vuelta_rotura
            #print('deuda detalles 2:...: ', deuda_detalles)

    # venta mas garantia mas detalles
    venta_garantia_detalles = venta_y_garantia + deuda_detalles

    # deuda en detalles
    saldo_venta = saldo_venta + deuda_detalles

    # saldo sin garantia
    saldo_sin_garantia = saldo_venta - venta.garantia_bs

    context = {
        'url_main': '',
        'venta': venta,
        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'error_anular': venta_controller.error_operation,
        'autenticado': 'si',
        'lista_aumentos': ventas_aumentos,
        'total_aumentos': total_aumentos,
        'lista_gastos': lista_gastos,
        'lista_ingresos': lista_ingresos,
        'saldo_venta': saldo_venta,
        'saldo_inicial': saldo_inicial,
        'venta_y_garantia': venta_y_garantia,
        'saldo_mas_gastos': saldo_mas_gastos,
        'saldo_sin_garantia': saldo_sin_garantia,
        'venta_garantia_detalles': venta_garantia_detalles,
        'deuda_detalles': deuda_detalles,
        'total_gastos': total_gastos,
        'total_cobros': total_cobros,
        'estado_anulado': venta_controller.anulado,
        'caja_usuario': caja_usuario,
        'fecha_actual': fecha_actual,

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'cobros',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/ventas_cobros.html', context)


# pasar a estado finalizado
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'modificar'), 'without_permission')
def ventas_pasar_finalizado(request, venta_id):
    # url modulo
    venta_check = Ventas.objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = Ventas.objects.get(pk=venta_id)

    # verificamos el estado
    if venta.status_id.status_id != venta_controller.vuelta_almacen:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'El registro debe estar en vuelta a almacen'}
        request.session.modified = True
        return False

    # confirma adicion gasto
    if 'pasar_finalizado_x' in request.POST.keys():
        if venta_controller.save(request, type='finalizado'):
            #messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Finalizado!', 'description': 'se finalizo la venta correctamente'})
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se realizo la finalizacion de la venta'}
            request.session.modified = True
            return True
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Finalizado!', 'description': venta_controller.error_operation})

    saldo_venta = venta_controller.saldo_venta(venta_id)

    context = {
        'url_main': '',
        'venta': venta,
        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'error_anular': venta_controller.error_operation,
        'autenticado': 'si',
        'saldo_venta': saldo_venta,
        'estado_anulado': venta_controller.anulado,

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'pasar_finalizado',
        'operation_x2': '',
        'operation_x3': '',
        'operation': venta_controller.finalizado,

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/ventas_finalizar.html', context)


# pasar finalizado anular
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'anular'), 'without_permission')
def ventas_pasar_finalizado_anular(request, venta_id):
    # url modulo
    venta_check = Ventas.objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = Ventas.objects.get(pk=venta_id)

    # verificamos el estado
    if venta.status_id.status_id != venta_controller.finalizado:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'El registro no es una venta finalizada'}
        request.session.modified = True
        return False

    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
    if not venta_controller.permission_operation(user_perfil, 'anular'):
        return render(request, 'pages/without_permission.html', {})

    # confirma anulacion
    if 'anular_x' in request.POST.keys():
        if venta_controller.can_anular(venta_id, user_perfil) and venta_controller.anular(request, venta_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se anulo la venta: '+request.POST['id']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    if venta_controller.can_anular(venta_id, user_perfil):
        puede_anular = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': 'No puede anular este registro, ' + venta_controller.error_operation})
        puede_anular = 0

    saldo_venta = venta_controller.saldo_venta(venta_id)

    context = {
        'url_main': '',
        'venta': venta,
        'saldo_venta': saldo_venta,
        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'puede_anular': puede_anular,
        'error_anular': venta_controller.error_operation,
        'autenticado': 'si',

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'pasar_finalizado_anular',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    context['operation'] = venta_controller.finalizado
    return render(request, 'ventas/ventas_finalizar.html', context)
