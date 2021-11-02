from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

# settings de la app
from django.conf import settings
from django.apps import apps

# propios
from cajas.models import CajasEgresos

# para los usuarios
# from permisos.models import Perfiles, Modulos, UsersModulos
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column, current_date
from utils.dates_functions import get_date_show

# controller por modulo
from controllers.ListasController import ListasController
from controllers.cajas.CajasController import CajasController
from controllers.cajas.CajasEgresosController import CajasEgresosController

# reportes
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportes.cajas.rptCajaEgresoRecibo import rptCajaEgresoRecibo


ce_controller = CajasEgresosController()


# cajas_egresos
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_CAJAS_EGRESOS, 'lista'), 'without_permission')
def cajas_egresos_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_CAJAS_EGRESOS)
    lista_controller = ListasController()

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'anular', 'print']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = cajas_egresos_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'anular':
            respuesta = cajas_egresos_anular(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'print':
            if permisos.imprimir:
                try:
                    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
                    if not ce_controller.permission_print(user_perfil, settings.MOD_CAJAS_EGRESOS, int(request.POST['id'].strip())):
                        return render(request, 'pages/without_permission.html', {})

                    buffer = io.BytesIO()
                    rptCajaEgresoRecibo(buffer, int(request.POST['id']))

                    buffer.seek(0)
                    # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
                    return FileResponse(buffer, filename='ce_recibo.pdf')

                except Exception as ex:
                    print('error al imprimir: ', str(ex))
                    request.session['internal_error'] = str(ex)
                    request.session.modified = True
                    return render(request, 'pages/internal_error.html', {'error': str(ex)})

            else:
                return render(request, 'pages/without_permission.html', {})

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    ce_lista = ce_controller.index(request)
    ce_session = request.session[ce_controller.modulo_session]
    estado_anulado = ce_controller.anulado

    cajas_lista = lista_controller.get_lista_cajas(request.user, settings.MOD_CAJAS_EGRESOS)
    # print(Cajas_lista)
    context = {
        'cajas_egresos': ce_lista,
        'session': ce_session,
        'permisos': permisos,
        'url_main': '',
        'cajas': cajas_lista,
        'estado_anulado': estado_anulado,
        'autenticado': 'si',

        'columnas': ce_controller.columnas,
        'js_file': ce_controller.modulo_session,

        'module_x': settings.MOD_CAJAS_EGRESOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'cajas/cajas_egresos.html', context)


# cajas_egresos add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_CAJAS_EGRESOS, 'adicionar'), 'without_permission')
def cajas_egresos_add(request):

    caja_controller = CajasController()
    caja_lista = caja_controller.cash_active(current_date(), request.user, formato_ori='yyyy-mm-dd')

    if not caja_lista:
        # no tiene caja activa
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Cajas Egresos!', 'description': 'Debe tener una caja activa'}
        request.session.modified = True
        return False

    caja_usuario = caja_lista[0]

    # balance del dia
    saldo_dia = caja_controller.day_balance(fecha=current_date(), Cajas=caja_usuario, formato_ori='yyyy-mm-dd')
    saldo_caja = saldo_dia[caja_usuario.caja_id]
    #print('saldo dia...: ', saldo_dia)

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if ce_controller.add(request):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Cajas Egresos!', 'description': 'Se agrego el nuevo egreso: '+request.POST['concepto']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas Egresos!', 'description': ce_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(CajasEgresos, '', request, None, 'concepto', 'monto')
    else:
        db_tags = get_html_column(CajasEgresos, '', None, None, 'concepto', 'monto')

    # lista de cajas
    #cajas_lista = lista_controller.get_lista_cajas(request.user, module='cajas_egresos')
    fecha_actual = get_date_show(fecha=current_date(), formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')

    context = {
        'url_main': '',
        'db_tags': db_tags,
        'control_form': ce_controller.control_form,
        'js_file': ce_controller.modulo_session,
        # 'Cajas': cajas_lista,
        'caja_usuario': caja_usuario,
        'fecha_actual': fecha_actual,
        'saldo_caja': saldo_caja,
        'autenticado': 'si',

        'module_x': settings.MOD_CAJAS_EGRESOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'cajas/cajas_egresos_form.html', context)


# cajas_egresos anular
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_CAJAS_EGRESOS, 'anular'), 'without_permission')
def cajas_egresos_anular(request, caja_egreso_id):

    ce_check = apps.get_model('cajas', 'CajasEgresos').objects.filter(pk=caja_egreso_id)
    if not ce_check:
        return render(request, 'pages/without_permission.html', {})

    caja_egreso = CajasEgresos.objects.get(pk=caja_egreso_id)

    # confirma eliminacion
    existe_error = False
    if 'anular_x' in request.POST.keys():
        if ce_controller.can_delete('caja_egreso_id', caja_egreso_id, **ce_controller.modelos_eliminar) and ce_controller.delete(request, caja_egreso_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Cajas Egresos!', 'description': 'Se anulo el egreso: '+request.POST['motivo_anula']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas Egresos!', 'description': ce_controller.error_operation})

    if ce_controller.can_delete('caja_egreso_id', caja_egreso_id, **ce_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas Egresos!', 'description': 'No puede anular este egreso, ' + ce_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(CajasEgresos, '', request, caja_egreso, 'concepto', 'monto', 'motivo_anula')
    else:
        db_tags = get_html_column(CajasEgresos, '', None, caja_egreso, 'concepto', 'monto', 'motivo_anula')

    context = {
        'url_main': '',
        'caja_egreso': caja_egreso,
        'db_tags': db_tags,
        'control_form': ce_controller.control_form,
        'js_file': ce_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': ce_controller.error_operation,
        'autenticado': 'si',

        'module_x': settings.MOD_CAJAS_EGRESOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'anular',
        'operation_x2': '',
        'operation_x3': '',

        'id': caja_egreso_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'cajas/cajas_egresos_form.html', context)
