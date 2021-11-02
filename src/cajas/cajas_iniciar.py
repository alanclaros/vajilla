from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

# settings de la app
from django.conf import settings
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
from reportes.cajas.rptCajasIniciar import rptCajasIniciar
# from reportes.cajas.rptCajasEntregar import rptCajasEntregar
# from reportes.cajas.rptCajaIngresoRecibo import rptCajaIngresoRecibo
# from reportes.cajas.rptCajaEgresoRecibo import rptCajaEgresoRecibo
# from reportes.cajas.rptCajaMovimientoRecibo import rptCajaMovimientoRecibo


caja_controller = CajasController()

# cajas iniciar index


@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_INICIAR_CAJA, 'lista'), 'without_permission')
def cajas_iniciar_index(request):
    # permisos
    permisos = get_permissions_user(request.user, settings.MOD_INICIAR_CAJA)
    #print('permisos: ', permisos)

    # impresion
    if 'operation_x' in request.POST.keys() and request.POST['operation_x'] == 'print':
        if permisos.imprimir:
            try:
                # Create a file-like buffer to receive PDF data.
                # print('id...', request.POST['id'])

                buffer = io.BytesIO()
                rptCajasIniciar(buffer, int(request.POST['id']))

                # # Create the PDF object, using the buffer as its "file."
                # p = canvas.Canvas(buffer)

                # # Draw things on the PDF. Here's where the PDF generation happens.
                # # See the ReportLab documentation for the full list of functionality.
                # p.drawString(100, 100, "Hello world.")

                # # Close the PDF object cleanly, and we're done.
                # p.showPage()
                # p.save()

                # FileResponse sets the Content-Disposition header so that browsers
                # present the option to save the file.
                buffer.seek(0)
                # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
                return FileResponse(buffer, filename='cajas_iniciar.pdf')

            except Exception as ex:
                print('error al imprimir: ', str(ex))
                return render(request, 'pages/without_permission.html', {})

        else:
            return render(request, 'pages/internal_error.html', {'error': str(ex)})

    # iniciar caja
    if 'operation_x' in request.POST.keys() and request.POST['operation_x'] == 'iniciar_x':
        if permisos.adicionar:
            try:
                caja = Cajas.objects.select_related('punto_id').get(pk=request.POST['id'])
                if caja_controller.add_operation('iniciar', current_date(), caja, formato_ori='yyyy-mm-dd'):
                    """si la caja esta en el estado no aperturado"""
                    monedas = caja_controller.get_coins(current_date(), caja, formato_ori='yyyy-mm-dd')
                    lista_monedas = ""
                    for moneda in monedas:
                        lista_monedas += str(moneda['moneda_id']) + '|' + str(moneda['monto']) + '||'

                    if len(lista_monedas) > 0:
                        lista_monedas = lista_monedas[0:len(lista_monedas)-2]

                    db_tags = get_html_column(CajasOperacionesDetalles, '', None, None, 'cantidad_apertura', 'cantidad_cierre')
                    context = {
                        'url_main': '',
                        'monedas': monedas,
                        'lista_monedas': lista_monedas,
                        'db_tags': db_tags,
                        'control_form': caja_controller.control_form,
                        'js_file': caja_controller.modulo_session,
                        'caja': caja,
                        'autenticado': 'si',
                        'current_date': get_date_show(fecha=current_date(), formato_ori='yyyy-mm-dd', formato='dd-MMM-yyyy'),

                        'module_x': settings.MOD_INICIAR_CAJA,
                        'module_x2': '',
                        'module_x3': '',

                        'operation_x': 'iniciar',
                        'operation_x2': '',
                        'operation_x3': '',

                        'id': caja.caja_id,
                        'id2': '',
                        'id3': '',
                    }
                    return render(request, 'cajas/cajas_iniciar_iniciando.html', context)
                else:
                    messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'la caja debe estar en estado no aperturado'})

            except Exception as ex:
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'error al inicar caja: ' + str(ex)})
        else:
            return render(request, 'pages/internal_error.html', {'error': str(ex)})

    # iniciar registrar
    if 'operation_x' in request.POST.keys() and request.POST['operation_x'] == 'iniciar_guardar_x':
        if permisos.adicionar:
            try:
                caja = Cajas.objects.get(pk=request.POST['id'])

                if caja_controller.save_data(current_date(), caja, 'iniciar_guardar', request, formato_ori='yyyy-mm-dd'):
                    # guardado
                    messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Cajas!', 'description': 'Se aperturo la Caja: ' + caja.caja})
                else:
                    messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'la caja debe estar en estado no aperturado'})

            except Exception as ex:
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'error al guardar inicio caja: ' + str(ex)})
        else:
            return render(request, 'pages/internal_error.html', {'error': str(ex)})

    # iniciar caja, cancelar
    if 'operation_x' in request.POST.keys() and request.POST['operation_x'] == 'cancelar_iniciar_x':
        if permisos.eliminar:
            try:
                caja = Cajas.objects.select_related('punto_id').get(pk=request.POST['id'])

                if caja_controller.add_operation('iniciar_cancelar', current_date(), caja, formato_ori='yyyy-mm-dd'):
                    """si la caja esta en el estado aperturado"""
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
                        total = total + (op.cantidad_apertura * op.moneda_id.monto)

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

                        'module_x': settings.MOD_INICIAR_CAJA,
                        'module_x2': '',
                        'module_x3': '',

                        'operation_x': 'iniciar_cancelar',
                        'operation_x2': '',
                        'operation_x3': '',

                        'id': caja.caja_id,
                        'id2': '',
                        'id3': '',
                    }
                    return render(request, 'cajas/cajas_iniciar_iniciando.html', context)
                else:
                    messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'la caja debe estar en estado aperturado'})

            except Exception as ex:
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'error al cancelar el inicio, ' + str(ex)})
        else:
            return render(request, 'pages/internal_error.html', {'error': str(ex)})

    # cancelar iniciar registrar
    if 'operation_x' in request.POST.keys() and request.POST['operation_x'] == 'cancelar_iniciar_guardar_x':
        if permisos.eliminar:
            try:
                caja = Cajas.objects.get(pk=request.POST['id'])

                if caja_controller.save_data(current_date(), caja, 'iniciar_cancelar', request, formato_ori='yyyy-mm-dd'):
                    # guardado
                    messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Cajas!', 'description': 'Se cancelo la apertura de la Caja: ' + caja.caja})
                else:
                    messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'la caja debe estar en estado aperturado para cancelarlo'})

            except Exception as ex:
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'error al cancelar el inicio, ' + str(ex)})
        else:
            return render(request, 'pages/internal_error.html', {'error': str(ex)})

    # datos por defecto de la ventana
    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
    cajas = caja_controller.index_operations(user_perfil, request.user, 'iniciar')
    # print(cajas)

    operaciones_caja = caja_controller.cash_status(current_date(), cajas, formato_ori='yyyy-mm-dd')
    # print(operacionesCaja)

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

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

        'module_x': settings.MOD_INICIAR_CAJA,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'cajas/cajas_iniciar.html', context)
