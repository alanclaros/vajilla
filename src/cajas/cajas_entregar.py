from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

# settings de la app
from django.conf import settings
from django.http import HttpResponseRedirect
from django.apps import apps

# propios
from configuraciones.models import Cajas
from status.models import Status
# para los usuarios
# from permisos.models import Perfiles, Modulos, UsersModulos
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column, current_date
from utils.dates_functions import get_date_show

from cajas.models import CajasOperaciones, CajasOperacionesDetalles

# controller por modulo
from controllers.ListasController import ListasController
from controllers.cajas.CajasController import CajasController

# reportes
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportes.cajas.rptCajasEntregar import rptCajasEntregar


caja_controller = CajasController()


# cajas entregar index
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_ENTREGAR_CAJA, 'lista'), 'without_permission')
def cajas_entregar_index(request):
    # permisos
    permisos = get_permissions_user(request.user, settings.MOD_ENTREGAR_CAJA)

    # impresion
    if 'operation_x' in request.POST.keys() and request.POST['operation_x'] == 'print':
        if permisos.imprimir:
            try:
                buffer = io.BytesIO()
                rptCajasEntregar(buffer, int(request.POST['id']))

                buffer.seek(0)
                # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
                return FileResponse(buffer, filename='cajas_entregar.pdf')
            except Exception as ex:
                print('error al imprimir: ', str(ex))
                return render(request, 'pages/internal_error.html', {'error': str(ex)})
        else:
            return render(request, 'pages/without_permission.html', {})

    # entregar caja
    if 'operation_x' in request.POST.keys() and request.POST['operation_x'] == 'entregar_x':
        if permisos.adicionar:
            try:
                caja = Cajas.objects.select_related('punto_id').get(pk=request.POST['id'])

                if caja_controller.add_operation('entregar', current_date(), caja, formato_ori='yyyy-mm-dd'):
                    """si la caja esta en el estado correcto"""
                    monedas = caja_controller.get_coins(current_date(), caja, formato_ori='yyyy-mm-dd')
                    lista_monedas = ""
                    for moneda in monedas:
                        lista_monedas += str(moneda['moneda_id'].moneda_id) + '|' + str(moneda['monto']) + '||'

                    if len(lista_monedas) > 0:
                        lista_monedas = lista_monedas[0:len(lista_monedas)-2]

                    # detalles
                    operacion = CajasOperaciones.objects.filter(caja_id=caja, fecha=current_date())[:1].get()
                    filtros = {}
                    filtros['caja_operacion_id'] = operacion
                    filtros['moneda_id__status_id_id'] = caja_controller.activo
                    detalle = CajasOperacionesDetalles.objects.select_related('moneda_id').filter(**filtros).order_by('moneda_id__monto')
                    # print(detalle)

                    db_tags = get_html_column(CajasOperacionesDetalles, '', None, None, 'cantidad_apertura', 'cantidad_cierre')
                    context = {
                        'url_main': '',
                        'monedas': monedas,
                        'lista_monedas': lista_monedas,
                        'db_tags': db_tags,
                        'control_form': caja_controller.control_form,
                        'js_file': caja_controller.modulo_session,
                        'caja': caja,
                        'detalle': detalle,
                        'autenticado': 'si',
                        'current_date': get_date_show(fecha=current_date(), formato_ori='yyyy-mm-dd', formato='dd-MMM-yyyy'),

                        'module_x': settings.MOD_ENTREGAR_CAJA,
                        'module_x2': '',
                        'module_x3': '',

                        'operation_x': 'entregar',
                        'operation_x2': '',
                        'operation_x3': '',

                        'id': caja.caja_id,
                        'id2': '',
                        'id3': '',
                    }
                    return render(request, 'cajas/cajas_entregar_form.html', context)
                else:
                    messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'la caja debe estar en estado apertura-recibe'})

            except Exception as ex:
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'error al devolver caja, ' + str(ex)})

        else:
            return render(request, 'pages/without_permission.html', {})

    # entregar registrar
    if 'operation_x' in request.POST.keys() and request.POST['operation_x'] == 'entregar_guardar_x':
        if permisos.adicionar:
            try:
                caja = Cajas.objects.get(pk=int(request.POST['id']))

                if caja_controller.save_data(current_date(), caja, 'entregar_guardar', request, formato_ori='yyyy-mm-dd'):
                    # guardado
                    messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Cajas!', 'description': 'Se entrego la Caja: ' + caja.caja})
                else:
                    messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'la caja debe estar en estado apertura-recibe'})

            except Exception as ex:
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'error al registrar la devolucion de caja, ' + str(ex)})

        else:
            return render(request, 'pages/without_permission.html', {})

    # entregar caja, cancelar
    if 'operation_x' in request.POST.keys() and request.POST['operation_x'] == 'cancelar_entregar_x':
        if permisos.eliminar:
            try:
                caja = Cajas.objects.select_related('punto_id').get(pk=int(request.POST['id']))

                if caja_controller.add_operation('entregar_cancelar', current_date(), caja, formato_ori='yyyy-mm-dd'):
                    """si la caja esta en el estado correcto"""
                    monedas = caja_controller.get_coins(current_date(), caja, formato_ori='yyyy-mm-dd')
                    # detalles
                    operacion = CajasOperaciones.objects.filter(caja_id=caja, fecha=current_date())[:1].get()
                    filtros = {}
                    filtros['caja_operacion_id'] = operacion
                    filtros['moneda_id__status_id_id'] = caja_controller.activo
                    detalle = CajasOperacionesDetalles.objects.select_related('moneda_id').filter(**filtros).order_by('moneda_id__monto')
                    # print(detalle)
                    total = 0
                    for op in detalle:
                        total = total + (op.cantidad_cierre * op.moneda_id.monto)

                    db_tags = get_html_column(CajasOperacionesDetalles, '', None, None, 'cantidad_apertura', 'cantidad_cierre')
                    context = {
                        'url_main': '',
                        'monedas': monedas,
                        'total': total,
                        'db_tags': db_tags,
                        'control_form': caja_controller.control_form,
                        'js_file': caja_controller.modulo_session,
                        'caja': caja,
                        'detalle': detalle,
                        'autenticado': 'si',
                        'current_date': get_date_show(fecha=current_date(), formato_ori='yyyy-mm-dd', formato='dd-MMM-yyyy'),

                        'module_x': settings.MOD_ENTREGAR_CAJA,
                        'module_x2': '',
                        'module_x3': '',

                        'operation_x': 'entregar_cancelar',
                        'operation_x2': '',
                        'operation_x3': '',

                        'id': caja.caja_id,
                        'id2': '',
                        'id3': '',
                    }
                    return render(request, 'cajas/cajas_entregar_form.html', context)
                else:
                    messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'la caja debe estar en estado cierre'})

            except Exception as ex:
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'error al cancelar el cierre de caja, ' + str(ex)})

        else:
            return render(request, 'pages/without_permission.html', {})

    # cancelar entregar registrar
    if 'operation_x' in request.POST.keys() and request.POST['operation_x'] == 'cancelar_entregar_guardar_x':
        if permisos.eliminar:
            try:
                caja = Cajas.objects.get(pk=request.POST['id'])

                if caja_controller.save_data(current_date(), caja, 'entregar_cancelar', request, formato_ori='yyyy-mm-dd'):
                    # guardado
                    messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Cajas!', 'description': 'Se cancelo la entrega de la Caja: ' + caja.caja})
                else:
                    messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'la caja debe estar en estado entrega para cancelarlo'})

            except Exception as ex:
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'error al cancelar el cierre de caja, ' + str(ex)})

        else:
            return render(request, 'pages/without_permission.html', {})

    # datos por defecto de la ventana
    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
    cajas = caja_controller.index_operations(user_perfil, request.user, 'entregar')
    # print(cajas)

    operaciones_caja = caja_controller.cash_status(current_date(), cajas, formato_ori='yyyy-mm-dd')
    # print(operacionesCaja)

    # estados
    apertura = caja_controller.apertura
    apertura_recibe = caja_controller.apertura_recibe
    cierre = caja_controller.cierre
    cierre_recibe = caja_controller.cierre_recibe
    no_aperturado = caja_controller.no_aperturado

    context = {
        'cajas': cajas,
        'operaciones_caja': operaciones_caja,
        'apertura': apertura,
        'apertura_recibe': apertura_recibe,
        'cierre': cierre,
        'cierre_recibe': cierre_recibe,
        'no_aperturado': no_aperturado,
        'permisos': permisos,
        'url_main': '',
        'autenticado': 'si',
        'current_date': get_date_show(fecha=current_date(), formato_ori='yyyy-mm-dd', formato='dd-MMM-yyyy'),
        'js_file': caja_controller.modulo_session,

        'module_x': settings.MOD_ENTREGAR_CAJA,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'cajas/cajas_entregar.html', context)
