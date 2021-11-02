import os
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
# settings de la app
from django.conf import settings
from django.apps import apps

# propios
from clientes.models import Clientes

# para los usuarios
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column

# controlador
from controllers.clientes.ClientesController import ClientesController


cliente_controller = ClientesController()


@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_CLIENTES, 'lista'), 'without_permission')
def clientes_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_CLIENTES)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'modify', 'delete']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = clientes_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = clientes_modify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'delete':
            respuesta = clientes_delete(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    clientes_lista = cliente_controller.index(request)
    # print(Ciudades)
    clientes_session = request.session[cliente_controller.modulo_session]
    # print(zonas_session)
    context = {
        'clientes': clientes_lista,
        'session': clientes_session,
        'permisos': permisos,
        'url_main': '',
        'js_file': cliente_controller.modulo_session,
        'autenticado': 'si',

        'columnas': cliente_controller.columnas,

        'module_x': settings.MOD_CLIENTES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'clientes/clientes.html', context)


# clientes add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_CLIENTES, 'adicionar'), 'without_permission')
def clientes_add(request):

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if cliente_controller.save(request):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Clientes!', 'description': 'Se agrego el nuevo cliente: '+request.POST['apellidos']+' '+request.POST['nombres']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Clientes!', 'description': cliente_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(Clientes, '', request, None, 'apellidos', 'nombres', 'ci_nit', 'email', 'direccion', 'telefonos', 'razon_social', 'factura_a')
    else:
        db_tags = get_html_column(Clientes, '', None, None, 'apellidos', 'nombres', 'ci_nit', 'email', 'direccion', 'telefonos', 'razon_social', 'factura_a')

    context = {
        'url_main': '',
        'operation_x': 'add',
        'db_tags': db_tags,
        'control_form': cliente_controller.control_form,
        'js_file': cliente_controller.modulo_session,
        'autenticado': 'si',
        'columnas': cliente_controller.columnas,

        'module_x': settings.MOD_CLIENTES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'clientes/clientes_form.html', context)


# clientes modify
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_CLIENTES, 'modificar'), 'without_permission')
def clientes_modify(request, cliente_id):
    cliente_check = apps.get_model('clientes', 'Clientes').objects.filter(pk=cliente_id)
    if not cliente_check:
        return render(request, 'pages/without_permission.html', {})

    cliente = Clientes.objects.get(pk=cliente_id)

    if cliente.status_id not in [cliente_controller.status_activo, cliente_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        if cliente_controller.save(request, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Clientes!', 'description': 'Se modifico el cliente: '+request.POST['apellidos']+' '+request.POST['nombres']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Clientes!', 'description': cliente_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(Clientes, '', request, cliente, 'apellidos', 'nombres', 'ci_nit', 'email', 'direccion', 'telefonos')
    else:
        db_tags = get_html_column(Clientes, '', None, cliente, 'apellidos', 'nombres', 'ci_nit', 'email', 'direccion', 'telefonos')

    context = {
        'url_main': '',
        'operation_x': 'modify',
        'cliente': cliente,
        'db_tags': db_tags,
        'control_form': cliente_controller.control_form,
        'js_file': cliente_controller.modulo_session,
        'autenticado': 'si',

        'module_x': settings.MOD_CLIENTES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': cliente_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'clientes/clientes_form.html', context)


# clientes delete
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_CLIENTES, 'eliminar'), 'without_permission')
def clientes_delete(request, cliente_id):
    cliente_check = apps.get_model('clientes', 'Clientes').objects.filter(pk=cliente_id)
    if not cliente_check:
        return render(request, 'pages/without_permission.html', {})

    cliente = get_object_or_404(Clientes, pk=cliente_id)

    # confirma eliminacion
    existe_error = False
    if 'delete_x' in request.POST.keys():
        if cliente_controller.can_delete('cliente_id', cliente_id, **cliente_controller.modelos_eliminar) and cliente_controller.delete(cliente_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Clientes!', 'description': 'Se elimino el cliente: '+request.POST['apellidos']+' '+request.POST['nombres']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Clientes!', 'description': cliente_controller.error_operation})

    if cliente_controller.can_delete('cliente_id', cliente_id, **cliente_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Clientes!', 'description': 'No puede eliminar este ciente, ' + cliente_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(Clientes, '', request, cliente, 'apellidos', 'nombres', 'ci_nit', 'email', 'direccion', 'telefonos')
    else:
        db_tags = get_html_column(Clientes, '', None, cliente, 'apellidos', 'nombres', 'ci_nit', 'email', 'direccion', 'telefonos')

    context = {
        'url_main': '',
        'operation_x': 'delete',
        'cliente': cliente,
        'db_tags': db_tags,
        'control_form': cliente_controller.control_form,
        'js_file': cliente_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': cliente_controller.error_operation,
        'autenticado': 'si',

        'module_x': settings.MOD_CLIENTES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'delete',
        'operation_x2': '',
        'operation_x3': '',

        'id': cliente_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'clientes/clientes_form.html', context)
