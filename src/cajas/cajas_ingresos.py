from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

# settings de la app
from django.conf import settings
from django.apps import apps

# propios
from cajas.models import CajasIngresos

# para los usuarios
# from permisos.models import Perfiles, Modulos, UsersModulos
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column, current_date
from utils.dates_functions import get_date_show, get_date_to_db

# controller por modulo
from controllers.ListasController import ListasController
from controllers.cajas.CajasController import CajasController
from controllers.cajas.CajasIngresosController import CajasIngresosController

# reportes
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportes.cajas.rptCajaIngresoRecibo import rptCajaIngresoRecibo

ci_controller = CajasIngresosController()


# cajas_ingresos
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_CAJAS_INGRESOS, 'lista'), 'without_permission')
def cajas_ingresos_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_CAJAS_INGRESOS)
    lista_controller = ListasController()

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'anular', 'print']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = cajas_ingresos_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'anular':
            respuesta = cajas_ingresos_anular(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'print':
            if permisos.imprimir:
                try:
                    # if not get_user_permission_operation(request.user, settings.MOD_CAJAS_INGRESOS, 'imprimir', 'caja_ingreso_id', int(request.POST['id'].strip()), 'cajas', 'CajasIngresos'):
                    #     return render(request, 'pages/without_permission.html', {})
                    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
                    if not ci_controller.permission_print(user_perfil, settings.MOD_CAJAS_INGRESOS, int(request.POST['id'].strip())):
                        return render(request, 'pages/without_permission.html', {})

                    buffer = io.BytesIO()
                    rptCajaIngresoRecibo(buffer, int(request.POST['id']))

                    buffer.seek(0)
                    return FileResponse(buffer, filename='ci_recibo.pdf')

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
    ci_lista = ci_controller.index(request)
    ci_session = request.session[ci_controller.modulo_session]
    estado_anulado = ci_controller.anulado

    # Cajas_lista = Cajas.objects.filter(status_id=status_activo, punto_id=UserP.punto_id).order_by('tipo_moneda_id_id')
    cajas_lista = lista_controller.get_lista_cajas(request.user, settings.MOD_CAJAS_INGRESOS)
    # print(zonas_session)
    context = {
        'cajas_ingresos': ci_lista,
        'session': ci_session,
        'permisos': permisos,
        'url_main': '',
        'cajas': cajas_lista,
        'estado_anulado': estado_anulado,
        'autenticado': 'si',

        'columnas': ci_controller.columnas,
        'js_file': ci_controller.modulo_session,

        'module_x': settings.MOD_CAJAS_INGRESOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'cajas/cajas_ingresos.html', context)


# cajas_ingresos add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_CAJAS_INGRESOS, 'adicionar'), 'without_permission')
def cajas_ingresos_add(request):
    caja_controller = CajasController()
    caja_lista = caja_controller.cash_active(current_date(), request.user, formato_ori='yyyy-mm-dd')

    if not caja_lista:
        # no tiene caja activa
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Cajas Ingresos!', 'description': 'Debe tener una caja activa'}
        request.session.modified = True
        return False

    caja_usuario = caja_lista[0]

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if ci_controller.add(request):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Cajas Ingresos!', 'description': 'Se agrego el nuevo ingreso: '+request.POST['concepto']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas Ingresos!', 'description': ci_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(CajasIngresos, '', request, None, 'concepto', 'monto')
    else:
        db_tags = get_html_column(CajasIngresos, '', None, None, 'concepto', 'monto')

    # lista de cajas
    # cajas_lista = lista_controller.get_lista_cajas(request.user, module='cajas_ingresos')
    fecha_actual = get_date_show(fecha=current_date(), formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')

    context = {
        'url_main': '',
        'db_tags': db_tags,
        'control_form': ci_controller.control_form,
        'js_file': ci_controller.modulo_session,
        # 'cajas': cajas_lista,
        'fecha_actual': fecha_actual,
        'caja_usuario': caja_usuario,
        'autenticado': 'si',

        'module_x': settings.MOD_CAJAS_INGRESOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'cajas/cajas_ingresos_form.html', context)


# cajas_ingresos anular
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_CAJAS_INGRESOS, 'anular'), 'without_permission')
def cajas_ingresos_anular(request, caja_ingreso_id):

    ci_check = apps.get_model('cajas', 'CajasIngresos').objects.filter(pk=caja_ingreso_id)
    if not ci_check:
        return render(request, 'pages/without_permission.html', {})

    caja_ingreso = CajasIngresos.objects.get(pk=caja_ingreso_id)

    # balance del dia
    caja_controller = CajasController()
    # print('caja...: ', caja_ingreso.caja_id)
    # print('fecha ant: ', caja_ingreso.fecha)
    # print('fecha...: ', get_date_to_db(fecha=caja_ingreso.fecha, formato='yyyy-mm-dd'))
    saldo_dia = caja_controller.day_balance(fecha=get_date_to_db(fecha=caja_ingreso.fecha, formato='yyyy-mm-dd'), Cajas=caja_ingreso.caja_id, formato_ori='yyyy-mm-dd')
    saldo_caja = saldo_dia[caja_ingreso.caja_id.caja_id]
    #print('saldo dia..: ', saldo_dia, ' ... saldo_caja: ', saldo_caja)

    # confirma eliminacion
    existe_error = False
    if 'anular_x' in request.POST.keys():
        if ci_controller.can_delete('caja_ingreso_id', caja_ingreso_id, **ci_controller.modelos_eliminar) and ci_controller.delete(request, caja_ingreso_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Cajas Ingresos!', 'description': 'Se anulo el ingreso: '+request.POST['motivo_anula']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas Ingresos!', 'description': ci_controller.error_operation})

    if ci_controller.can_delete('caja_ingreso_id', caja_ingreso_id, **ci_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas Ingresos!', 'description': 'No puede anular este ingreso, ' + ci_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(CajasIngresos, '', request, caja_ingreso, 'concepto', 'monto', 'motivo_anula')
    else:
        db_tags = get_html_column(CajasIngresos, '', None, caja_ingreso, 'concepto', 'monto', 'motivo_anula')

    context = {
        'url_main': '',
        'caja_ingreso': caja_ingreso,
        'db_tags': db_tags,
        'control_form': ci_controller.control_form,
        'js_file': ci_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': ci_controller.error_operation,
        'autenticado': 'si',
        'saldo_caja': saldo_caja,

        'module_x': settings.MOD_CAJAS_INGRESOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'anular',
        'operation_x2': '',
        'operation_x3': '',

        'id': caja_ingreso_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'cajas/cajas_ingresos_form.html', context)
