from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.contrib import messages

# utils
from utils.permissions import get_user_permission_operation, get_permissions_user

# clases
from controllers.configuraciones.ConfiguracionesController import ConfiguracionesController

# controlador del modulo
configuracion_controller = ConfiguracionesController()


# configuraciones
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_CONFIGURACIONES_SISTEMA, 'lista'), 'without_permission')
def configuraciones_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_CONFIGURACIONES_SISTEMA)

    if 'operation_x' in request.POST.keys() and request.POST['operation_x'] == 'modify':
        if permisos.modificar:
            if configuracion_controller.save(request):
                messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Configuraciones!', 'description': 'Datos Guardados Correctamente'})
            else:
                # error al actualizar
                existe_error = True
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Configuraciones!', 'description': configuracion_controller.error_operation})
        else:
            return render(request, 'pages/without_permission.html', {})

    # datos por defecto
    configuraciones_lista = configuracion_controller.index(request)
    context = {
        'configuraciones': configuraciones_lista,
        'js_file': configuracion_controller.modulo_session,
        'control_form': configuracion_controller.control_form,
        'permisos': permisos,
        'url_main': '',
        'autenticado': 'si',

        'module_x': settings.MOD_CONFIGURACIONES_SISTEMA,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': '1',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/configuraciones.html', context)
