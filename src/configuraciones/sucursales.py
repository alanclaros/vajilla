from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.apps import apps
from django.conf import settings
from django.contrib import messages

# utils
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column

# clases
from controllers.configuraciones.SucursalesController import SucursalesController
from controllers.configuraciones.AlmacenesController import AlmacenesController

# controlador del modulo
sucursal_controller = SucursalesController()
almacen_controller = AlmacenesController()


# sucursales
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_SUCURSALES, 'lista'), 'without_permission')
def sucursales_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_SUCURSALES)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'modify', 'delete', 'almacenes']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = sucursales_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = sucursales_modify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'delete':
            respuesta = sucursales_delete(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'almacenes':
            respuesta = almacenes_index(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto

    sucursales_lista = sucursal_controller.index(request)
    sucursales_session = request.session[sucursal_controller.modulo_session]

    context = {
        'sucursales': sucursales_lista,
        'session': sucursales_session,
        'permisos': permisos,
        'url_main': '',
        'js_file': sucursal_controller.modulo_session,
        'autenticado': 'si',

        'columnas': sucursal_controller.columnas,

        'module_x': settings.MOD_SUCURSALES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/sucursales.html', context)


# sucursales add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_SUCURSALES, 'adicionar'), 'without_permission')
def sucursales_add(request):

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if sucursal_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Sucursales!', 'description': 'Se agrego la nueva sucursal: '+request.POST['sucursal']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Sucursales!', 'description': sucursal_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Sucursales'), 'email', request, None, 'sucursal', 'codigo', 'email', 'empresa', 'direccion', 'telefonos', 'actividad')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Sucursales'), 'email', None, None, 'sucursal', 'codigo', 'email', 'empresa', 'direccion', 'telefonos', 'actividad')

    context = {
        'url_main': '',
        'db_tags': db_tags,
        'control_form': sucursal_controller.control_form,
        'js_file': sucursal_controller.modulo_session,
        'ciudad': 1,
        'autenticado': 'si',

        'module_x': settings.MOD_SUCURSALES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/sucursales_form.html', context)


# sucursales modify
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_SUCURSALES, 'modificar'), 'without_permission')
def sucursales_modify(request, sucursal_id):
    # url modulo
    sucursal_check = apps.get_model('configuraciones', 'Sucursales').objects.filter(pk=sucursal_id)
    if not sucursal_check:
        return render(request, 'pages/without_permission.html', {})

    sucursal = apps.get_model('configuraciones', 'Sucursales').objects.get(pk=sucursal_id)

    if sucursal.status_id not in [sucursal_controller.status_activo, sucursal_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        if sucursal_controller.save(request, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Sucursales!', 'description': 'Se modifico la sucursal: '+request.POST['sucursal']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Sucursales!', 'description': sucursal_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Sucursales'), 'email', request, sucursal, 'sucursal', 'codigo', 'email', 'empresa', 'direccion', 'telefonos', 'actividad')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Sucursales'), 'email', None, sucursal, 'sucursal', 'codigo', 'email', 'empresa', 'direccion', 'telefonos', 'actividad')

    context = {
        'url_main': '',
        'sucursal': sucursal,
        'db_tags': db_tags,
        'control_form': sucursal_controller.control_form,
        'js_file': sucursal_controller.modulo_session,
        'ciudad': 1,
        'status_active': sucursal_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_SUCURSALES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': sucursal_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/sucursales_form.html', context)


# sucursales delete
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_SUCURSALES, 'eliminar'), 'without_permission')
def sucursales_delete(request, sucursal_id):
    # url modulo
    sucursal_check = apps.get_model('configuraciones', 'Sucursales').objects.filter(pk=sucursal_id)
    if not sucursal_check:
        return render(request, 'pages/without_permission.html', {})

    sucursal = apps.get_model('configuraciones', 'Sucursales').objects.get(pk=sucursal_id)

    if sucursal.status_id not in [sucursal_controller.status_activo, sucursal_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # confirma eliminacion
    existe_error = False
    if 'delete_x' in request.POST.keys():
        if sucursal_controller.can_delete('sucursal_id', sucursal_id, **sucursal_controller.modelos_eliminar) and sucursal_controller.delete(sucursal_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Sucursales!', 'description': 'Se elimino la sucursal: '+request.POST['sucursal']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Sucursales!', 'description': sucursal_controller.error_operation})

    if sucursal_controller.can_delete('sucursal_id', sucursal_id, **sucursal_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Sucursales!', 'description': 'No puede eliminar esta sucursal, ' + sucursal_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Sucursales'), 'email', request, sucursal, 'sucursal', 'codigo', 'email', 'empresa', 'direccion', 'telefonos', 'actividad')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Sucursales'), 'email', None, sucursal, 'sucursal', 'codigo', 'email', 'empresa', 'direccion', 'telefonos', 'actividad')

    context = {
        'url_main': '',
        'sucursal': sucursal,
        'db_tags': db_tags,
        'control_form': sucursal_controller.control_form,
        'js_file': sucursal_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': sucursal_controller.error_operation,
        'ciudad': 1,
        'status_active': sucursal_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_SUCURSALES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'delete',
        'operation_x2': '',
        'operation_x3': '',

        'id': sucursal_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/sucursales_form.html', context)


# almacenes
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_SUCURSALES, 'lista'), 'without_permission')
def almacenes_index(request, sucursal_id):
    permisos = get_permissions_user(request.user, settings.MOD_SUCURSALES)

    # operaciones
    if 'operation_x2' in request.POST.keys():
        operation = request.POST['operation_x2']
        if not operation in ['', 'add', 'modify', 'delete']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = almacenes_add(request, sucursal_id)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = almacenes_modify(request, sucursal_id, request.POST['id2'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'delete':
            respuesta = almacenes_delete(request, sucursal_id, request.POST['id2'])
            if not type(respuesta) == bool:
                return respuesta

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    almacenes_lista = almacen_controller.index(request, sucursal_id)
    almacenes_session = request.session[almacen_controller.modulo_session]
    # datos de la sucursal
    sucursal_dato = apps.get_model('configuraciones', 'Sucursales').objects.select_related('ciudad_id').get(pk=sucursal_id)

    context = {
        'almacenes': almacenes_lista,
        'sucursal_dato': sucursal_dato,
        'session': almacenes_session,
        'permisos': permisos,
        'url_main': '',
        'url_sucursales': '',
        'js_file': almacen_controller.modulo_session,
        'autenticado': 'si',

        'columnas': almacen_controller.columnas,
        'module_x': settings.MOD_SUCURSALES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'almacenes',
        'operation_x2': '',
        'operation_x3': '',

        'id': sucursal_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/almacenes.html', context)


# almacenes add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_SUCURSALES, 'adicionar'), 'without_permission')
def almacenes_add(request, sucursal_id):

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if almacen_controller.save(request, sucursal_id, type='add'):
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

    # datos de la sucursal
    sucursal_dato = apps.get_model('configuraciones', 'Sucursales').objects.select_related('ciudad_id').get(pk=sucursal_id)

    context = {
        'url_main': '',
        'url_sucursales': '',
        'db_tags': db_tags,
        'control_form': almacen_controller.control_form,
        'js_file': almacen_controller.modulo_session,
        'sucursal_dato': sucursal_dato,
        'autenticado': 'si',

        'module_x': settings.MOD_SUCURSALES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'almacenes',
        'operation_x2': 'add',
        'operation_x3': '',

        'id': sucursal_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/almacenes_form.html', context)


# almacenes modify
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_SUCURSALES, 'modificar'), 'without_permission')
def almacenes_modify(request, sucursal_id, almacen_id):
    # url modulo
    almacen_check = apps.get_model('configuraciones', 'Almacenes').objects.filter(pk=almacen_id)
    if not almacen_check:
        return render(request, 'pages/without_permission.html', {})

    almacen = apps.get_model('configuraciones', 'Almacenes').objects.get(pk=almacen_id)
    almacen_controller = AlmacenesController()

    if almacen.status_id not in [almacen_controller.status_activo, almacen_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        if almacen_controller.save(request, sucursal_id, type='modify'):
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

    # datos de la sucursal
    sucursal_dato = apps.get_model('configuraciones', 'Sucursales').objects.select_related('ciudad_id').get(pk=sucursal_id)

    context = {
        'url_main': '',
        'url_sucursales': '',
        'almacen': almacen,
        'db_tags': db_tags,
        'control_form': almacen_controller.control_form,
        'js_file': almacen_controller.modulo_session,
        'sucursal_dato': sucursal_dato,
        'status_active': almacen_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_SUCURSALES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'almacenes',
        'operation_x2': 'modify',
        'operation_x3': '',

        'id': sucursal_id,
        'id2': almacen_id,
        'id3': '',
    }
    return render(request, 'configuraciones/almacenes_form.html', context)


# almacenes delete
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_SUCURSALES, 'eliminar'), 'without_permission')
def almacenes_delete(request, sucursal_id, almacen_id):
    # url modulo
    almacen_check = apps.get_model('configuraciones', 'Almacenes').objects.filter(pk=almacen_id)
    if not almacen_check:
        return render(request, 'pages/without_permission.html', {})

    almacen = apps.get_model('configuraciones', 'Almacenes').objects.get(pk=almacen_id)
    almacen_controller = AlmacenesController()

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

    # datos de la sucursal
    sucursal_dato = apps.get_model('configuraciones', 'Sucursales').objects.select_related('ciudad_id').get(pk=sucursal_id)

    context = {
        'url_main': '',
        'url_sucursales': '',
        'almacen': almacen,
        'db_tags': db_tags,
        'control_form': almacen_controller.control_form,
        'js_file': almacen_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': almacen_controller.error_operation,
        'sucursal_dato': sucursal_dato,
        'status_active': almacen_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_SUCURSALES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'almacenes',
        'operation_x2': 'delete',
        'operation_x3': '',

        'id': sucursal_id,
        'id2': almacen_id,
        'id3': '',
    }
    return render(request, 'configuraciones/almacenes_form.html', context)
