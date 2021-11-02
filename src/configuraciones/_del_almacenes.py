from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.apps import apps
from django.conf import settings
from django.contrib import messages

# utils
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column

# clases
from controllers.configuraciones.AlmacenesController import AlmacenesController

# modelo
from configuraciones.models import Almacenes

# controlador del modulo
almacen_controller = AlmacenesController()


# almacenes
# almacenes
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_ALMACENES, 'lista'), 'without_permission')
def almacenes_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_ALMACENES)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'modify', 'delete']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = almacenes_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = almacenes_modify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'delete':
            respuesta = almacenes_delete(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    almacenes_lista = almacen_controller.index(request)
    almacenes_session = request.session[almacen_controller.modulo_session]
    # print(zonas_session)
    context = {
        'almacenes': almacenes_lista,
        'session': almacenes_session,
        'permisos': permisos,
        'autenticado': 'si',

        'columnas': almacen_controller.columnas,

        'js_file': almacen_controller.modulo_session,
        'module_x': settings.MOD_ALMACENES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/almacenes.html', context)


# almacenes add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_ALMACENES, 'adicionar'), 'without_permission')
def almacenes_add(request):

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if almacen_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Almacenes!', 'description': 'Se agrego el nuevo almacen: '+request.POST['almacen']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Almacenes!', 'description': almacen_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Almacenes'), '', request, None, 'almacen', 'codigo')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Almacenes'), '', None, None, 'almacen', 'codigo')

    # lista de sucursales
    sucursales_lista = apps.get_model('configuraciones', 'Sucursales').objects.filter(status_id=almacen_controller.status_activo).order_by('sucursal')

    context = {
        'url_main': 'url_main',
        'operation_x': 'add',
        'sucursales_lista': sucursales_lista,
        'db_tags': db_tags,
        'control_form': almacen_controller.control_form,
        'js_file': almacen_controller.modulo_session,
        'autenticado': 'si',

        'module_x': settings.MOD_ALMACENES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/almacenes_form.html', context)


# almacenes modify
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_ALMACENES, 'modificar'), 'without_permission')
def almacenes_modify(request, almacen_id):
    # url modulo
    almacen_check = Almacenes.objects.filter(pk=almacen_id)
    if not almacen_check:
        return render(request, 'pages/without_permission.html', {})

    almacen = apps.get_model('configuraciones', 'Almacenes').objects.get(pk=almacen_id)

    if almacen.status_id not in [almacen_controller.status_activo, almacen_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        if almacen_controller.save(request, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Almacenes!', 'description': 'Se modifico el almacen: '+request.POST['almacen']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Almacenes!', 'description': almacen_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Almacenes'), '', request, almacen, 'almacen', 'codigo')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Almacenes'), '', None, almacen, 'almacen', 'codigo')

    # lista de almacens
    sucursales_lista = apps.get_model('configuraciones', 'Sucursales').objects.filter(status_id=almacen_controller.status_activo).order_by('sucursal')

    context = {
        'url_main': 'url_main',
        'operation_x': 'modify',
        'almacen': almacen,
        'sucursales_lista': sucursales_lista,
        'db_tags': db_tags,
        'control_form': almacen_controller.control_form,
        'js_file': almacen_controller.modulo_session,
        'status_active': almacen_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_ALMACENES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': almacen_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/almacenes_form.html', context)


# almacenes delete
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_ALMACENES, 'eliminar'), 'without_permission')
def almacenes_delete(request, almacen_id):
    # url modulo
    almacen_check = Almacenes.objects.filter(pk=almacen_id)
    if not almacen_check:
        return render(request, 'pages/without_permission.html', {})

    almacen = Almacenes.objects.get(pk=almacen_id)

    if almacen.status_id not in [almacen_controller.status_activo, almacen_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # confirma eliminacion
    existe_error = False
    if 'delete_x' in request.POST.keys():
        if almacen_controller.can_delete('almacen_id', almacen_id, **almacen_controller.modelos_eliminar) and almacen_controller.delete(almacen_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Almacenes!', 'description': 'Se elimino el almacen: '+request.POST['almacen']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Almacenes!', 'description': almacen_controller.error_operation})

    if almacen_controller.can_delete('almacen_id', almacen_id, **almacen_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Almacenes!', 'description': 'No puede eliminar este almacen, ' + almacen_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Almacenes'), '', request, almacen, 'almacen', 'codigo')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Almacenes'), '', None, almacen, 'almacen', 'codigo')

    # lista de almacens
    sucursales_lista = apps.get_model('configuraciones', 'Sucursales').objects.filter(status_id=almacen_controller.status_activo).order_by('sucursal')

    context = {
        'url_main': '',
        'operation_x': 'delete',
        'almacen': almacen,
        'sucursales_lista': sucursales_lista,
        'db_tags': db_tags,
        'control_form': almacen_controller.control_form,
        'js_file': almacen_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': almacen_controller.error_operation,
        'status_active': almacen_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_ALMACENES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'delete',
        'operation_x2': '',
        'operation_x3': '',

        'id': almacen_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/almacenes_form.html', context)
