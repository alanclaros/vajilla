from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.apps import apps
from django.conf import settings
from django.contrib import messages

# utils
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column

# clases
from controllers.configuraciones.LineasController import LineasController

# modelo
from configuraciones.models import Lineas

# controlador del modulo
linea_controller = LineasController()


# lineas
# lineas
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_LINEAS, 'lista'), 'without_permission')
def lineas_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_LINEAS)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'modify', 'delete', 'mostrar_imagen']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = lineas_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = lineas_modify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'delete':
            respuesta = lineas_delete(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'mostrar_imagen':
            linea_imagen = Lineas.objects.get(pk=int(request.POST['id']))
            context_img = {
                'linea_imagen': linea_imagen,
                'autenticado': 'si',
            }
            return render(request, 'configuraciones/lineas_imagenes_mostrar.html', context_img)

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    lineas_lista = linea_controller.index(request)
    lineas_session = request.session[linea_controller.modulo_session]
    # print(zonas_session)
    context = {
        'lineas': lineas_lista,
        'session': lineas_session,
        'permisos': permisos,
        'autenticado': 'si',

        'columnas': linea_controller.columnas,

        'js_file': linea_controller.modulo_session,
        'module_x': settings.MOD_LINEAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/lineas.html', context)


# lineas add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_LINEAS, 'adicionar'), 'without_permission')
def lineas_add(request):

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if linea_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Lineas!', 'description': 'Se agrego la nueva linea: '+request.POST['linea']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Lineas!', 'description': linea_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Lineas'), 'descripcion', request, None, 'linea', 'codigo', 'descripcion')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Lineas'), 'descripcion', None, None, 'linea', 'codigo', 'descripcion')

    # lista de lineas
    lineas_lista = Lineas.objects.filter(status_id=linea_controller.status_activo).order_by('linea')

    context = {
        'url_main': 'url_main',
        'operation_x': 'add',
        'lineas_lista': lineas_lista,
        'db_tags': db_tags,
        'control_form': linea_controller.control_form,
        'js_file': linea_controller.modulo_session,
        'autenticado': 'si',

        'module_x': settings.MOD_LINEAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/lineas_form.html', context)


# lineas modify
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_LINEAS, 'modificar'), 'without_permission')
def lineas_modify(request, linea_id):
    # url modulo
    linea_check = Lineas.objects.filter(pk=linea_id)
    if not linea_check:
        return render(request, 'pages/without_permission.html', {})

    linea = apps.get_model('configuraciones', 'Lineas').objects.get(pk=linea_id)

    if linea.status_id not in [linea_controller.status_activo, linea_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        if linea_controller.save(request, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Lineas!', 'description': 'Se modifico la linea: '+request.POST['linea']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Lineas!', 'description': linea_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Lineas'), 'descripcion', request, linea, 'linea', 'codigo', 'descripcion')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Lineas'), 'descripcion', None, linea, 'linea', 'codigo', 'descripcion')

    # lista de lineas
    lineas_lista = Lineas.objects.filter(status_id=linea_controller.status_activo).exclude(pk=linea_id).order_by('linea')

    context = {
        'url_main': 'url_main',
        'operation_x': 'modify',
        'linea': linea,
        'lineas_lista': lineas_lista,
        'db_tags': db_tags,
        'control_form': linea_controller.control_form,
        'js_file': linea_controller.modulo_session,
        'status_active': linea_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_LINEAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': linea_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/lineas_form.html', context)


# lineas delete
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_LINEAS, 'eliminar'), 'without_permission')
def lineas_delete(request, linea_id):
    # url modulo
    linea_check = Lineas.objects.filter(pk=linea_id)
    if not linea_check:
        return render(request, 'pages/without_permission.html', {})

    linea = apps.get_model('configuraciones', 'Lineas').objects.get(pk=linea_id)

    if linea.status_id not in [linea_controller.status_activo, linea_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # confirma eliminacion
    existe_error = False
    if 'delete_x' in request.POST.keys():
        if linea_controller.can_delete('linea_id', linea_id, **linea_controller.modelos_eliminar) and linea_controller.delete(linea_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Lineas!', 'description': 'Se elimino la linea: '+request.POST['linea']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Lineas!', 'description': linea_controller.error_operation})

    if linea_controller.can_delete('linea_id', linea_id, **linea_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Lineas!', 'description': 'No puede eliminar esta linea, ' + linea_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Lineas'), 'descripcion', request, linea, 'linea', 'codigo', 'descripcion')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Lineas'), 'descripcion', None, linea, 'linea', 'codigo', 'descripcion')

    context = {
        'url_main': '',
        'operation_x': 'delete',
        'linea': linea,
        'db_tags': db_tags,
        'control_form': linea_controller.control_form,
        'js_file': linea_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': linea_controller.error_operation,
        'status_active': linea_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_LINEAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'delete',
        'operation_x2': '',
        'operation_x3': '',

        'id': linea_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/lineas_form.html', context)
