from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

# settings de la app
from django.conf import settings

# para los usuarios
from utils.permissions import get_user_permission_operation, get_permissions_user

# clases por modulo
from controllers.ventas.PendientesController import PendientesController

pendiente_controller = PendientesController()


# pendientes
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'lista'), 'without_permission')
def pendientes_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_VENTAS)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'modify', 'anular']:
            return render(request, 'pages/without_permission.html', {})

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    ventas_lista = pendiente_controller.index(request)
    ventas_session = request.session[pendiente_controller.modulo_session]

    # print(zonas_session)
    context = {
        'ventas': ventas_lista,
        'session': ventas_session,
        'permisos': permisos,
        'url_main': '',
        'estado_anulado': pendiente_controller.anulado,
        'estado_preventa': pendiente_controller.preventa,
        'estado_venta': pendiente_controller.venta,
        'estado_salida': pendiente_controller.salida_almacen,
        'estado_vuelta': pendiente_controller.vuelta_almacen,
        'estado_finalizado': pendiente_controller.finalizado,
        'autenticado': 'si',

        'js_file': pendiente_controller.modulo_session,
        'columnas': pendiente_controller.columnas,
        'module_x': settings.MOD_PENDIENTES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'ventas/pendientes.html', context)
