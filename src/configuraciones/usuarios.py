
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.apps import apps
from django.conf import settings
from django.contrib import messages
from permisos.models import UsersPerfiles

# utils
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column

# clases
from controllers.permisos.UsuariosController import UsuariosController
from controllers.ListasController import ListasController

# controlador del modulo
usuario_controller = UsuariosController()


@ user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_USUARIOS, 'lista'), 'without_permission')
def usuarios_index(request):
    """usuarios index"""
    permisos = get_permissions_user(request.user, settings.MOD_USUARIOS)
    # usuario_controller = UsuariosController()

    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']

        # operaciones permitidas
        if not operation in ['', 'add', 'modify', 'delete']:
            return render(request, 'pages/without_permission.html', {})

        # add
        if operation == 'add':
            respuesta = usuarios_add(request)
            if not type(respuesta) == bool:
                return respuesta

        # modify
        if operation == 'modify':
            respuesta = usuarios_modify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        # delete
        if operation == 'delete':
            respuesta = usuarios_delete(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    usuarios_perfiles = usuario_controller.index(request)
    usuario_session = request.session[usuario_controller.modulo_session]

    # actualizando permisos
    permisos = get_permissions_user(request.user, settings.MOD_USUARIOS)

    context = {
        # 'usuarios': usuarios,
        'usuarios_perfiles': usuarios_perfiles,
        'session': usuario_session,
        'columnas': usuario_controller.columnas,
        'permisos': permisos,
        'url_main': 'url_main',
        'autenticado': 'si',

        'js_file': usuario_controller.modulo_session,
        'module_x': settings.MOD_USUARIOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }

    return render(request, 'configuraciones/usuarios.html', context)


# usuarios add
@ user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_USUARIOS, 'adicionar'), 'without_permission')
def usuarios_add(request):
    """add usuarios"""
    lista_controller = ListasController()

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if usuario_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Usuarios!', 'description': 'Se agrego el nuevo usuario: '+request.POST['username']}
            request.session.modified = True
            # return HttpResponseRedirect(url_main)
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Usuarios!', 'description': usuario_controller.error_operation})

    # modulos
    modulos = lista_controller.get_lista_modulos(request.user, settings.MOD_USUARIOS)
    #user_modulos = {}
    perfiles = lista_controller.get_lista_perfiles(request.user, settings.MOD_USUARIOS)

    # cajas
    cajas = lista_controller.get_lista_cajas(request.user, settings.MOD_PUNTOS)
    # puntos
    puntos = lista_controller.get_lista_puntos(request.user, settings.MOD_PUNTOS)

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('auth', 'User'), 'email', request, None, 'first_name', 'last_name', 'username', 'email')
    else:
        db_tags = get_html_column(apps.get_model('auth', 'User'), 'email', None, None, 'first_name', 'last_name', 'username', 'email')

    # modulos del sistemas
    modulos_sistema = {}

    modulos_sistema[settings.MOD_VENTAS] = {'modulo': 1, 'adiciona': 1, 'modifica': 1, 'elimina': 0, 'anula': 1, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_PRODUCTOS] = {'modulo': 1, 'adiciona': 1, 'modifica': 1, 'elimina': 1, 'anula': 0, 'imprime': 0, 'permiso': 0}
    modulos_sistema[settings.MOD_PENDIENTES] = {'modulo': 1, 'adiciona': 0, 'modifica': 0, 'elimina': 0, 'anula': 0, 'imprime': 0, 'permiso': 0}
    modulos_sistema[settings.MOD_CLIENTES] = {'modulo': 1, 'adiciona': 1, 'modifica': 1, 'elimina': 1, 'anula': 0, 'imprime': 0, 'permiso': 0}

    modulos_sistema[settings.MOD_INICIAR_CAJA] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 1, 'anula': 0, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_INICIAR_CAJA_RECIBIR] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 1, 'anula': 0, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_ENTREGAR_CAJA] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 1, 'anula': 0, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_ENTREGAR_CAJA_RECIBIR] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 1, 'anula': 0, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_CAJAS_MOVIMIENTOS] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 0, 'anula': 1, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_CAJAS_INGRESOS] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 0, 'anula': 1, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_CAJAS_EGRESOS] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 0, 'anula': 1, 'imprime': 1, 'permiso': 0}

    modulos_sistema[settings.MOD_INGRESOS_ALMACEN] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 0, 'anula': 1, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_SALIDAS_ALMACEN] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 0, 'anula': 1, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_MOVIMIENTOS_ALMACEN] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 0, 'anula': 1, 'imprime': 1, 'permiso': 0}

    modulos_sistema[settings.MOD_USUARIOS] = {'modulo': 1, 'adiciona': 1, 'modifica': 1, 'elimina': 1, 'anula': 0, 'imprime': 0, 'permiso': 0}
    modulos_sistema[settings.MOD_LINEAS] = {'modulo': 1, 'adiciona': 1, 'modifica': 1, 'elimina': 1, 'anula': 0, 'imprime': 0, 'permiso': 0}
    modulos_sistema[settings.MOD_CONFIGURACIONES_SISTEMA] = {'modulo': 1, 'adiciona': 0, 'modifica': 1, 'elimina': 0, 'anula': 0, 'imprime': 0, 'permiso': 0}
    modulos_sistema[settings.MOD_SUCURSALES] = {'modulo': 1, 'adiciona': 1, 'modifica': 1, 'elimina': 1, 'anula': 0, 'imprime': 0, 'permiso': 0}
    modulos_sistema[settings.MOD_PUNTOS] = {'modulo': 1, 'adiciona': 1, 'modifica': 1, 'elimina': 1, 'anula': 0, 'imprime': 0, 'permiso': 0}

    modulos_sistema[settings.MOD_TABLAS_BACKUP] = {'modulo': 1, 'adiciona': 0, 'modifica': 0, 'elimina': 0, 'anula': 0, 'imprime': 0, 'permiso': 0}
    modulos_sistema[settings.MOD_REPORTES] = {'modulo': 1, 'adiciona': 0, 'modifica': 0, 'elimina': 0, 'anula': 0, 'imprime': 1, 'permiso': 1}

    #print('modulos_sistema: ', modulos_sistema)

    context = {
        'modulos_sistema': modulos_sistema,

        'url_main': '',
        'perfiles': perfiles,
        'modulos': modulos,
        'cajas': cajas,
        'puntos': puntos,
        # 'user_modulos': user_modulos,
        'db_tags': db_tags,
        'control_form': usuario_controller.control_form,
        'js_file': usuario_controller.modulo_session,
        'autenticado': 'si',

        'module_x': settings.MOD_USUARIOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/usuario.html', context)


# usuarios modify
@ user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_USUARIOS, 'modificar'), 'without_permission')
def usuarios_modify(request, id):
    """modify usuario"""
    # url modulo
    usuario_check = UsersPerfiles.objects.filter(pk=id)
    if not usuario_check:
        return render(request, 'pages/without_permission.html', {})

    usuario_perfil = UsersPerfiles.objects.get(pk=id)

    if usuario_perfil.status_id not in [usuario_controller.status_activo, usuario_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    lista_controller = ListasController()

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        if usuario_controller.save(request, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Usuarios!', 'description': 'Se modifico el usuario: '+request.POST['username']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Usuarios!', 'description': usuario_controller.error_operation})

    # modulos
    modulos = lista_controller.get_lista_modulos(request.user, settings.MOD_USUARIOS)
    user_modulos = apps.get_model('permisos', 'UsersModulos').objects.filter(user_perfil_id=usuario_perfil)
    perfiles = lista_controller.get_lista_perfiles(request.user, settings.MOD_USUARIOS)

    # cajas
    cajas = lista_controller.get_lista_cajas(request.user, settings.MOD_PUNTOS)
    # puntos
    puntos = lista_controller.get_lista_puntos(request.user, settings.MOD_PUNTOS)
    # usuario
    usuario = apps.get_model('auth', 'User').objects.get(pk=usuario_perfil.user_id.id)

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('auth', 'User'), 'email', request, usuario, 'first_name', 'last_name', 'username', 'email')
    else:
        db_tags = get_html_column(apps.get_model('auth', 'User'), 'email', None, usuario, 'first_name', 'last_name', 'username', 'email')

    # modulos del sistemas
    modulos_sistema = {}

    modulos_sistema[settings.MOD_VENTAS] = {'modulo': 1, 'adiciona': 1, 'modifica': 1, 'elimina': 0, 'anula': 1, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_PRODUCTOS] = {'modulo': 1, 'adiciona': 1, 'modifica': 1, 'elimina': 1, 'anula': 0, 'imprime': 0, 'permiso': 0}
    modulos_sistema[settings.MOD_PENDIENTES] = {'modulo': 1, 'adiciona': 0, 'modifica': 0, 'elimina': 0, 'anula': 0, 'imprime': 0, 'permiso': 0}
    modulos_sistema[settings.MOD_CLIENTES] = {'modulo': 1, 'adiciona': 1, 'modifica': 1, 'elimina': 1, 'anula': 0, 'imprime': 0, 'permiso': 0}

    modulos_sistema[settings.MOD_INICIAR_CAJA] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 1, 'anula': 0, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_INICIAR_CAJA_RECIBIR] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 1, 'anula': 0, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_ENTREGAR_CAJA] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 1, 'anula': 0, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_ENTREGAR_CAJA_RECIBIR] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 1, 'anula': 0, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_CAJAS_MOVIMIENTOS] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 0, 'anula': 1, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_CAJAS_INGRESOS] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 0, 'anula': 1, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_CAJAS_EGRESOS] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 0, 'anula': 1, 'imprime': 1, 'permiso': 0}

    modulos_sistema[settings.MOD_INGRESOS_ALMACEN] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 0, 'anula': 1, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_SALIDAS_ALMACEN] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 0, 'anula': 1, 'imprime': 1, 'permiso': 0}
    modulos_sistema[settings.MOD_MOVIMIENTOS_ALMACEN] = {'modulo': 1, 'adiciona': 1, 'modifica': 0, 'elimina': 0, 'anula': 1, 'imprime': 1, 'permiso': 0}

    modulos_sistema[settings.MOD_USUARIOS] = {'modulo': 1, 'adiciona': 1, 'modifica': 1, 'elimina': 1, 'anula': 0, 'imprime': 0, 'permiso': 0}
    modulos_sistema[settings.MOD_LINEAS] = {'modulo': 1, 'adiciona': 1, 'modifica': 1, 'elimina': 1, 'anula': 0, 'imprime': 0, 'permiso': 0}
    modulos_sistema[settings.MOD_CONFIGURACIONES_SISTEMA] = {'modulo': 1, 'adiciona': 0, 'modifica': 1, 'elimina': 0, 'anula': 0, 'imprime': 0, 'permiso': 0}
    modulos_sistema[settings.MOD_SUCURSALES] = {'modulo': 1, 'adiciona': 1, 'modifica': 1, 'elimina': 1, 'anula': 0, 'imprime': 0, 'permiso': 0}
    modulos_sistema[settings.MOD_PUNTOS] = {'modulo': 1, 'adiciona': 1, 'modifica': 1, 'elimina': 1, 'anula': 0, 'imprime': 0, 'permiso': 0}

    modulos_sistema[settings.MOD_TABLAS_BACKUP] = {'modulo': 1, 'adiciona': 0, 'modifica': 0, 'elimina': 0, 'anula': 0, 'imprime': 0, 'permiso': 0}
    modulos_sistema[settings.MOD_REPORTES] = {'modulo': 1, 'adiciona': 0, 'modifica': 0, 'elimina': 0, 'anula': 0, 'imprime': 1, 'permiso': 1}

    context = {
        'modulos_sistema': modulos_sistema,

        'url_main': 'url_main',
        'operation_x': 'modify',
        'perfiles': perfiles,
        'cajas': cajas,
        'puntos': puntos,
        'modulos': modulos,
        'user_modulos': user_modulos,
        'usuario': usuario,
        'usuario_perfil': usuario_perfil,
        'db_tags': db_tags,
        'control_form': usuario_controller.control_form,
        'js_file': usuario_controller.modulo_session,
        'status_active': usuario_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_USUARIOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/usuario.html', context)


# usuarios delete
@ user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_USUARIOS, 'eliminar'), 'without_permission')
def usuarios_delete(request, id):
    """delete usuario"""
    usuario_check = UsersPerfiles.objects.filter(pk=id)
    if not usuario_check:
        return render(request, 'pages/without_permission.html', {})

    usuario_perfil = UsersPerfiles.objects.get(pk=id)

    if usuario_perfil.status_id not in [usuario_controller.status_activo, usuario_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    #usuario_controller = UsuariosController()
    lista_controller = ListasController()

    # guardamos
    existe_error = False
    if 'delete_x' in request.POST.keys():
        if usuario_controller.can_delete('user_perfil_id', id, **usuario_controller.modelos_eliminar) and usuario_controller.delete(id):
            # if usuario_controller.modify(request, id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Usuarios!', 'description': 'Se elimino el usuario: '+request.POST['username']}
            request.session.modified = True
            # return HttpResponseRedirect(url_main)
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Usuarios!', 'description': usuario_controller.error_operation})

    # modulos
    modulos = lista_controller.get_lista_modulos(request.user, settings.MOD_USUARIOS)
    user_modulos = apps.get_model('permisos', 'UsersModulos').objects.filter(user_perfil_id=usuario_perfil)
    perfiles = lista_controller.get_lista_perfiles(request.user, settings.MOD_USUARIOS)

    # cajas
    cajas = lista_controller.get_lista_cajas(request.user, settings.MOD_PUNTOS)
    # puntos
    puntos = lista_controller.get_lista_puntos(request.user, settings.MOD_PUNTOS)
    # usuario
    usuario = apps.get_model('auth', 'User').objects.get(pk=usuario_perfil.user_id.id)

    if usuario_controller.can_delete('user_perfil_id', id, **usuario_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Usuarios!', 'description': 'No puede eliminar este usuario, ' + usuario_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('auth', 'User'), 'email', request, usuario, 'first_name', 'last_name', 'username', 'email')
    else:
        db_tags = get_html_column(apps.get_model('auth', 'User'), 'email', None, usuario, 'first_name', 'last_name', 'username', 'email')

    context = {
        'url_main': 'url_main',
        'operation_x': 'delete',
        'perfiles': perfiles,
        'cajas': cajas,
        'puntos': puntos,
        'modulos': modulos,
        'user_modulos': user_modulos,
        'usuario': usuario,
        'db_tags': db_tags,
        'control_form': usuario_controller.control_form,
        'js_file': usuario_controller.modulo_session,
        'status_active': usuario_controller.activo,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': usuario_controller.error_operation,
        'usuario_perfil': usuario_perfil,
        'autenticado': 'si',

        'module_x': settings.MOD_USUARIOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'delete',
        'operation_x2': '',
        'operation_x3': '',

        'id': id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/usuario.html', context)
