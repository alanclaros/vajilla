from utils.dates_functions import get_date_show
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
# settings de la app
from django.conf import settings
from django.http import HttpResponseRedirect
from django.apps import apps

# propios
from cajas.models import Cajas, CajasMovimientos

# para los usuarios
# from permisos.models import Perfiles, Modulos, UsersModulos
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column, current_date
#from utils.dates_functions import get_date_show

# controller por modulo
from controllers.ListasController import ListasController
from controllers.cajas.CajasController import CajasController
from controllers.cajas.CajasMovimientosController import CajasMovimientosController

# reportes
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportes.cajas.rptCajaMovimientoRecibo import rptCajaMovimientoRecibo

caja_movimiento_controller = CajasMovimientosController()


# cajas movimientos index
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_CAJAS_MOVIMIENTOS, 'lista'), 'without_permission')
def cajas_movimientos_index(request):
    caja_controller = CajasController()

    # permisos
    permisos = get_permissions_user(request.user, settings.MOD_CAJAS_MOVIMIENTOS)

    # impresion
    if 'operation_x' in request.POST.keys() and request.POST['operation_x'] == 'print':
        if permisos.imprimir:
            try:
                buffer = io.BytesIO()
                rptCajaMovimientoRecibo(buffer, int(request.POST['id']))

                buffer.seek(0)
                # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
                return FileResponse(buffer, filename='cajas_movimiento.pdf')

            except Exception as ex:
                print('error al imprimir: ', str(ex))
                request.session['internal_error'] = str(ex)
                request.session.modified = True
                return render(request, 'pages/without_permission.html', {'error': str(ex)})
        else:
            return render(request, 'pages/without_permission.html', {})

    # adicionar envio
    if 'operation_x' in request.POST.keys() and (request.POST['operation_x'] == 'add' or request.POST['operation_x'] == 'add_guardar'):
        if permisos.adicionar:
            operation = request.POST['operation_x']
            error = 0

            if operation == 'add_guardar':
                if caja_movimiento_controller.add(current_date(), request):
                    # guardado
                    request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Cajas Movimientos!', 'description': 'Se registro el movimiento de envio'}
                    request.session.modified = True
                    # return True
                else:
                    messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas Movimientos!', 'description': caja_movimiento_controller.error_operation})
                    error = 1

            # datos por defecto de la ventana
            if error == 1 or operation == 'add':
                user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
                punto_actual = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)

                caja_origen = Cajas.objects.select_related('tipo_moneda_id').get(pk=user_perfil.caja_id)
                saldo_origen_caja = caja_controller.day_balance(current_date(), caja_origen, formato_ori='yyyy-mm-dd')
                saldo_origen = saldo_origen_caja[caja_origen.caja_id]

                filtro = {}
                filtro['punto_id__sucursal_id'] = punto_actual.sucursal_id
                filtro['status_id'] = caja_movimiento_controller.status_activo

                cajas_destino = Cajas.objects.select_related('punto_id').filter(**filtro).exclude(punto_id=punto_actual).order_by('punto_id__punto', 'codigo')
                cajas_estado = caja_controller.cash_status(current_date(), cajas_destino, formato_ori='yyyy-mm-dd')

                # print(cajas)
                db_tags = get_html_column(CajasMovimientos, '', None, None, 'concepto', 'monto')
                context = {
                    'url_main': '',
                    'db_tags': db_tags,
                    'control_form': caja_movimiento_controller.control_form,
                    'js_file': caja_movimiento_controller.modulo_session,

                    'caja_origen': caja_origen,
                    'saldo_origen': saldo_origen,
                    'cajas_destino': cajas_destino,
                    'cajas_estado': cajas_estado,

                    'apertura_recibe': caja_movimiento_controller.apertura_recibe,
                    'autenticado': 'si',
                    'current_date': get_date_show(fecha=current_date(), formato_ori='yyyy-mm-dd', formato='dd-MMM-yyyy'),

                    'module_x': settings.MOD_CAJAS_MOVIMIENTOS,
                    'module_x2': '',
                    'module_x3': '',

                    'operation_x': 'add',
                    'operation_x2': '',
                    'operation_x3': '',

                    'id': '',
                    'id2': '',
                    'id3': '',
                }
                return render(request, 'cajas/cajas_movimientos_enviar.html', context)

        else:
            return render(request, 'pages/without_permission.html', {})

    # anular envio
    if 'operation_x' in request.POST.keys() and (request.POST['operation_x'] == 'anular' or request.POST['operation_x'] == 'anular_guardar'):
        if permisos.anular:
            operation = request.POST['operation_x']
            error = 0
            # datos
            caja_movimiento_dato = CajasMovimientos.objects.select_related('caja1_id').select_related('caja1_user_perfil_id').select_related(
                'caja2_id').select_related('caja2_user_perfil_id').select_related('tipo_moneda_id').get(pk=int(request.POST['id']))

            # verificamos estado correcto
            if caja_movimiento_dato.status_id.status_id != caja_movimiento_controller.movimiento_caja:
                # ingreso no autorizado
                return render(request, 'pages/without_permission.html', {})

            if operation == 'anular_guardar':
                if caja_movimiento_controller.anular_envio(request, request.POST['id']):
                    # guardado
                    #messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Cajas Movimientos!', 'description': 'Se anulo el movimiento de envio'})
                    request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Cajas Movimientos!', 'description': 'Se anulo el movimiento de envio'}
                    request.session.modified = True
                    # return True
                else:
                    messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas Movimientos!', 'description': caja_movimiento_controller.error_operation})
                    error = 1

            # datos por defecto de la ventana
            if error == 1 or operation == 'anular':
                #UserPerfil = get_datos_usuario(request)
                #PuntoActual = Puntos.objects.get(pk=UserPerfil.punto_id)

                # print(cajas)
                db_tags = get_html_column(CajasMovimientos, '', None, None, 'concepto', 'monto')
                context = {
                    'url_main': '',
                    'db_tags': db_tags,
                    'control_form': caja_movimiento_controller.control_form,
                    'js_file': caja_movimiento_controller.modulo_session,
                    'puede_anular': 1,
                    'cm_dato': caja_movimiento_dato,
                    'autenticado': 'si',
                    'current_date': get_date_show(fecha=current_date(), formato_ori='yyyy-mm-dd', formato='dd-MMM-yyyy'),

                    'module_x': settings.MOD_CAJAS_MOVIMIENTOS,
                    'module_x2': '',
                    'module_x3': '',

                    'operation_x': 'anular',
                    'operation_x2': '',
                    'operation_x3': '',

                    'id': caja_movimiento_dato.caja_movimiento_id,
                    'id2': '',
                    'id3': '',
                }
                return render(request, 'cajas/cajas_movimientos_enviar.html', context)

        else:
            return render(request, 'pages/without_permission.html', {})

    # aceptar recepcion
    if 'operation_x' in request.POST.keys() and (request.POST['operation_x'] == 'aceptar_recepcion_x' or request.POST['operation_x'] == 'aceptar_recepcion_guardar'):
        if permisos.adicionar:
            operation = request.POST['operation_x']
            error = 0
            # datos
            caja_movimiento_dato = CajasMovimientos.objects.select_related('caja1_id').select_related('caja1_user_perfil_id').select_related(
                'caja2_id').select_related('caja2_user_perfil_id').select_related('tipo_moneda_id').get(pk=int(request.POST['id']))

            # verificamos estado correcto
            if caja_movimiento_dato.status_id.status_id != caja_movimiento_controller.movimiento_caja:
                # ingreso no autorizado
                return render(request, 'pages/without_permission.html', {})

            if operation == 'aceptar_recepcion_guardar':
                if caja_movimiento_controller.aceptar_recepcion(request, request.POST['id']):
                    # guardado
                    #messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Cajas Movimientos!', 'description': 'Se acepto el envio de caja'})
                    request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Cajas Movimientos!', 'description': 'Se acepto el envio de caja'}
                    request.session.modified = True
                    # return True
                else:
                    messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas Movimientos!', 'description': caja_movimiento_controller.error_operation})
                    error = 1

            # datos por defecto de la ventana
            if error == 1 or operation == 'aceptar_recepcion_x':
                #UserPerfil = get_datos_usuario(request)
                #PuntoActual = Puntos.objects.get(pk=UserPerfil.punto_id)

                # print(cajas)
                db_tags = get_html_column(CajasMovimientos, '', None, None, 'concepto', 'monto')
                context = {
                    'url_main': '',
                    'db_tags': db_tags,
                    'control_form': caja_movimiento_controller.control_form,
                    'js_file': caja_movimiento_controller.modulo_session,
                    'cm_dato': caja_movimiento_dato,
                    'autenticado': 'si',
                    'current_date': get_date_show(fecha=current_date(), formato_ori='yyyy-mm-dd', formato='dd-MMM-yyyy'),

                    'module_x': settings.MOD_CAJAS_MOVIMIENTOS,
                    'module_x2': '',
                    'module_x3': '',

                    'operation_x': 'aceptar_recepcion',
                    'operation_x2': '',
                    'operation_x3': '',

                    'id': caja_movimiento_dato.caja_movimiento_id,
                    'id2': '',
                    'id3': '',
                }
                return render(request, 'cajas/cajas_movimientos_recibir.html', context)

        else:
            return render(request, 'pages/internal_error.html', {'error': str(ex)})

    # anular, aceptar recepcion
    if 'operation_x' in request.POST.keys() and (request.POST['operation_x'] == 'anular_recepcion_x' or request.POST['operation_x'] == 'anular_recepcion_guardar'):
        if permisos.anular:
            operation = request.POST['operation_x']
            error = 0
            # datos
            caja_movimiento_dato = CajasMovimientos.objects.select_related('caja1_id').select_related('caja1_user_perfil_id').select_related(
                'caja2_id').select_related('caja2_user_perfil_id').select_related('tipo_moneda_id').get(pk=int(request.POST['id']))

            # verificamos estado correcto
            if caja_movimiento_dato.status_id.status_id != caja_movimiento_controller.movimiento_caja_recibe:
                # ingreso no autorizado
                return render(request, 'pages/without_permission.html', {})

            if operation == 'anular_recepcion_guardar':
                if caja_movimiento_controller.anular_recepcion(request, request.POST['id']):
                    # guardado
                    #messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Cajas Movimientos!', 'description': 'Se anula la recepcion del envio'})
                    request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Cajas Movimientos!', 'description': 'Se anulo la recepcioin del envio'}
                    request.session.modified = True
                    # return True
                else:
                    messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas Movimientos!', 'description': caja_movimiento_controller.error_operation})
                    error = 1

            # datos por defecto de la ventana
            if error == 1 or operation == 'anular_recepcion_x':
                db_tags = get_html_column(CajasMovimientos, '', None, None, 'concepto', 'monto')
                context = {
                    'url_main': '',
                    'db_tags': db_tags,
                    'control_form': caja_movimiento_controller.control_form,
                    'js_file': caja_movimiento_controller.modulo_session,
                    'cm_dato': caja_movimiento_dato,
                    'puede_anular': 1,
                    'autenticado': 'si',
                    'current_date': get_date_show(fecha=current_date(), formato_ori='yyyy-mm-dd', formato='dd-MMM-yyyy'),

                    'module_x': settings.MOD_CAJAS_MOVIMIENTOS,
                    'module_x2': '',
                    'module_x3': '',

                    'operation_x': 'anular_recepcion',
                    'operation_x2': '',
                    'operation_x3': '',

                    'id': caja_movimiento_dato.caja_movimiento_id,
                    'id2': '',
                    'id3': '',
                }
                return render(request, 'cajas/cajas_movimientos_recibir.html', context)

        else:
            return render(request, 'pages/without_permission.html', {})

    # datos por defecto de la ventana
    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
    punto_actual = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)
    #print('envios lista...')
    movimientos_envios_lista = caja_movimiento_controller.index_envio(punto_actual, request)
    movimientos_recepcion_lista = caja_movimiento_controller.index_recepcion(punto_actual, request)

    # estados
    movimiento_caja = caja_movimiento_controller.movimiento_caja
    movimiento_caja_recibe = caja_movimiento_controller.movimiento_caja_recibe
    estado_anulado = caja_movimiento_controller.anulado

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    context = {
        'movimiento_caja': movimiento_caja,
        'movimiento_caja_recibe': movimiento_caja_recibe,
        'estado_anulado': estado_anulado,
        'permisos': permisos,
        'url_main': '',
        'envios_lista': movimientos_envios_lista,
        'recepcion_lista': movimientos_recepcion_lista,
        'autenticado': 'si',
        'current_date': get_date_show(fecha=current_date(), formato_ori='yyyy-mm-dd', formato='dd-MMM-yyyy'),
        'user_perfil': user_perfil,

        'js_file': caja_controller.modulo_session,

        'module_x': settings.MOD_CAJAS_MOVIMIENTOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'cajas/cajas_movimientos.html', context)
