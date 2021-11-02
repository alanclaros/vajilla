from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.apps import apps
from django.conf import settings
from django.contrib import messages

# utils
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column

# clases
from controllers.configuraciones.PuntosController import PuntosController
from controllers.configuraciones.CajasConfiguracionesController import CajasConfiguracionesController
from controllers.ListasController import ListasController

# modelo
from configuraciones.models import Puntos

# controlador del modulo
punto_controller = PuntosController()
caja_configuracion_controller = CajasConfiguracionesController()


# puntos
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PUNTOS, 'lista'), 'without_permission')
def puntos_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_PUNTOS)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'modify', 'delete', 'cajas', 'puntos_almacenes']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = puntos_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = puntos_modify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'delete':
            respuesta = puntos_delete(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'cajas':
            respuesta = cajas_index(request, request.POST['id'])
            return respuesta

        if operation == 'puntos_almacenes':
            respuesta = puntos_almacenes_index(request, request.POST['id'])
            return respuesta

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    puntos_lista = punto_controller.index(request)
    puntos_session = request.session[punto_controller.modulo_session]

    context = {
        'puntos': puntos_lista,
        'session': puntos_session,
        'permisos': permisos,
        'url_main': '',
        'js_file': punto_controller.modulo_session,
        'autenticado': 'si',

        'columnas': punto_controller.columnas,

        'module_x': settings.MOD_PUNTOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/puntos.html', context)


# puntos add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PUNTOS, 'adicionar'), 'without_permission')
def puntos_add(request):
    # lista controller
    lista_controller = ListasController()

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if punto_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Puntos!', 'description': 'Se agrego el nuevo punto: '+request.POST['punto']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Puntos!', 'description': punto_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Puntos'), '', request, None, 'punto', 'codigo')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Puntos'), '', None, None, 'punto', 'codigo')

    # lista de sucursales
    sucursales_lista = lista_controller.get_lista_sucursales(request.user)

    context = {
        'url_main': '',
        'db_tags': db_tags,
        'control_form': punto_controller.control_form,
        'js_file': punto_controller.modulo_session,
        'sucursales': sucursales_lista,
        'autenticado': 'si',

        'module_x': settings.MOD_PUNTOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/puntos_form.html', context)


# puntos modify
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PUNTOS, 'modificar'), 'without_permission')
def puntos_modify(request, punto_id):

    punto_check = Puntos.objects.filter(pk=punto_id)
    if not punto_check:
        return render(request, 'pages/without_permission.html', {})

    punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=punto_id)
    lista_controller = ListasController()

    if punto.status_id not in [punto_controller.status_activo, punto_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        if punto_controller.save(request, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Puntos!', 'description': 'Se modifico el punto: '+request.POST['punto']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Puntos!', 'description': punto_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Puntos'), '', request, punto, 'punto', 'codigo')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Puntos'), '', None, punto, 'punto', 'codigo')

    # lista de sucursales
    sucursales_lista = lista_controller.get_lista_sucursales(request.user)

    context = {
        'url_main': '',
        'punto': punto,
        'db_tags': db_tags,
        'control_form': punto_controller.control_form,
        'js_file': punto_controller.modulo_session,
        'sucursales': sucursales_lista,
        'status_active': punto_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_PUNTOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': punto_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/puntos_form.html', context)


# puntos delete
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PUNTOS, 'eliminar'), 'without_permission')
def puntos_delete(request, punto_id):
    # url modulo
    punto_check = Puntos.objects.filter(pk=punto_id)
    if not punto_check:
        return render(request, 'pages/without_permission.html', {})

    punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=punto_id)
    lista_controller = ListasController()

    if punto.status_id not in [punto_controller.status_activo, punto_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # confirma eliminacion
    existe_error = False
    if 'delete_x' in request.POST.keys():
        if punto_controller.can_delete('punto_id', punto_id, **punto_controller.modelos_eliminar) and punto_controller.delete(punto_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Puntos!', 'description': 'Se elimino el punto: '+request.POST['punto']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Puntos!', 'description': punto_controller.error_operation})

    if punto_controller.can_delete('punto_id', punto_id, **punto_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Puntos!', 'description': 'No puede eliminar este punto, ' + punto_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Puntos'), '', request, punto, 'punto', 'codigo')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Puntos'), '', None, punto, 'punto', 'codigo')

    # lista de sucursales
    sucursales_lista = lista_controller.get_lista_sucursales(request.user)

    context = {
        'url_main': '',
        'punto': punto,
        'db_tags': db_tags,
        'control_form': punto_controller.control_form,
        'js_file': punto_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': punto_controller.error_operation,
        'sucursales': sucursales_lista,
        'status_active': punto_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_PUNTOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'delete',
        'operation_x2': '',
        'operation_x3': '',

        'id': punto_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/puntos_form.html', context)


# cajas
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PUNTOS, 'modificar'), 'without_permission')
def cajas_index(request, punto_id):
    permisos = get_permissions_user(request.user, settings.MOD_PUNTOS)

    # operaciones
    if 'operation_x2' in request.POST.keys():
        operation = request.POST['operation_x2']
        if not operation in ['', 'add', 'modify', 'delete']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = cajas_add(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = cajas_modify(request, request.POST['id'], request.POST['id2'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'delete':
            respuesta = cajas_delete(request, request.POST['id'], request.POST['id2'])
            if not type(respuesta) == bool:
                return respuesta

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    cajas_lista = caja_configuracion_controller.index(request, punto_id)
    # print(Ciudades)
    cajas_session = request.session[caja_configuracion_controller.modulo_session]
    punto_caja = apps.get_model('configuraciones', 'Puntos').objects.get(pk=punto_id)

    context = {
        'cajas': cajas_lista,
        'session': cajas_session,
        'permisos': permisos,
        'url_main': '',
        'url_puntos': '',
        'punto_caja': punto_caja,
        'js_file': caja_configuracion_controller.modulo_session,
        'autenticado': 'si',

        'columnas': caja_configuracion_controller.columnas,

        'module_x': settings.MOD_PUNTOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'cajas',
        'operation_x2': '',
        'operation_x3': '',

        'id': punto_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/cajas.html', context)


# cajas add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PUNTOS, 'modificar'), 'without_permission')
def cajas_add(request, punto_id):
    # lista controller
    lista_controller = ListasController()

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if caja_configuracion_controller.save(request, punto_id, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Cajas!', 'description': 'Se agrego la nueva caja: '+request.POST['caja']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': caja_configuracion_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Cajas'), '', request, None, 'caja', 'codigo')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Cajas'), '', None, None, 'caja', 'codigo')

    # lista de tipos monedas
    tipos_monedas_lista = lista_controller.get_lista_tipos_monedas(request.user)

    # datos del punto
    punto_caja = apps.get_model('configuraciones', 'Puntos').objects.select_related('sucursal_id').select_related('sucursal_id__ciudad_id').get(pk=punto_id)

    context = {
        'url_main': '',
        'url_puntos': '',
        'db_tags': db_tags,
        'control_form': caja_configuracion_controller.control_form,
        'js_file': caja_configuracion_controller.modulo_session,
        'tipos_monedas': tipos_monedas_lista,
        'punto_caja': punto_caja,
        'autenticado': 'si',

        'module_x': settings.MOD_PUNTOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'cajas',
        'operation_x2': 'add',
        'operation_x3': '',

        'id': punto_id,
        'id2': '',
        'id3': '',

    }
    return render(request, 'configuraciones/cajas_form.html', context)


# cajas modify
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PUNTOS, 'modificar'), 'without_permission')
def cajas_modify(request, punto_id, caja_id):
    # url modulo
    caja_check = apps.get_model('configuraciones', 'Cajas').objects.filter(pk=caja_id)
    if not caja_check:
        return render(request, 'pages/without_permission.html', {})

    caja = apps.get_model('configuraciones', 'Cajas').objects.get(pk=caja_id)
    lista_controller = ListasController()

    if caja.status_id not in [caja_configuracion_controller.status_activo, caja_configuracion_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        if caja_configuracion_controller.save(request, punto_id, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Cajas!', 'description': 'Se modifico la caja: '+request.POST['caja']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': caja_configuracion_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Cajas'), '', request, caja, 'caja', 'codigo')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Cajas'), '', None, caja, 'caja', 'codigo')

    # tipos monedas lista
    tipos_monedas_lista = lista_controller.get_lista_tipos_monedas(request.user)

    # datos del punto
    punto_caja = apps.get_model('configuraciones', 'Puntos').objects.select_related('sucursal_id').select_related('sucursal_id__ciudad_id').get(pk=punto_id)

    context = {
        'url_main': '',
        'url_puntos': '',
        'caja': caja,
        'db_tags': db_tags,
        'control_form': caja_configuracion_controller.control_form,
        'js_file': caja_configuracion_controller.modulo_session,
        'tipos_monedas': tipos_monedas_lista,
        'punto_caja': punto_caja,
        'status_active': caja_configuracion_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_PUNTOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'cajas',
        'operation_x2': 'modify',
        'operation_x3': '',

        'id': punto_id,
        'id2': caja_id,
        'id3': '',
    }
    return render(request, 'configuraciones/cajas_form.html', context)


# cajas delete
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PUNTOS, 'eliminar'), 'without_permission')
def cajas_delete(request, punto_id, caja_id):
    # url modulo
    caja_check = apps.get_model('configuraciones', 'Cajas').objects.filter(pk=caja_id)
    if not caja_check:
        return render(request, 'pages/without_permission.html', {})

    caja = apps.get_model('configuraciones', 'Cajas').objects.get(pk=caja_id)
    lista_controller = ListasController()

    if caja.status_id not in [caja_configuracion_controller.status_activo, caja_configuracion_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # confirma eliminacion
    existe_error = False
    if 'delete_x' in request.POST.keys():
        if caja_configuracion_controller.can_delete('caja_id', caja_id, **caja_configuracion_controller.modelos_eliminar) and caja_configuracion_controller.delete(caja_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Cajas!', 'description': 'Se elimino la caja: '+request.POST['caja']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': caja_configuracion_controller.error_operation})

    if caja_configuracion_controller.can_delete('caja_id', caja_id, **caja_configuracion_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cajas!', 'description': 'No puede eliminar esta caja, ' + caja_configuracion_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Cajas'), '', request, caja, 'caja', 'codigo')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Cajas'), '', None, caja, 'caja', 'codigo')

    # lista de tipos monedas
    tipos_monedas_lista = lista_controller.get_lista_tipos_monedas(request.user)

    # datos del punto
    punto_caja = apps.get_model('configuraciones', 'Puntos').objects.select_related('sucursal_id').select_related('sucursal_id__ciudad_id').get(pk=punto_id)

    context = {
        'url_main': '',
        'url_puntos': '',
        'caja': caja,
        'db_tags': db_tags,
        'control_form': caja_configuracion_controller.control_form,
        'js_file': caja_configuracion_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': caja_configuracion_controller.error_operation,
        'tipos_monedas': tipos_monedas_lista,
        'punto_caja': punto_caja,
        'status_active': caja_configuracion_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_PUNTOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'cajas',
        'operation_x2': 'delete',
        'operation_x3': '',

        'id': punto_id,
        'id2': caja_id,
        'id3': '',
    }
    return render(request, 'configuraciones/cajas_form.html', context)


# puntos almacenes
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PUNTOS, 'lista'), 'without_permission')
def puntos_almacenes_index(request, punto_id):
    permisos = get_permissions_user(request.user, settings.MOD_PUNTOS)
    lista_controller = ListasController()

    punto_check = apps.get_model('configuraciones', 'Puntos').objects.filter(pk=punto_id)
    if not punto_check:
        return render(request, 'pages/without_permission.html', {})

    punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=punto_id)
    if punto.status_id not in [punto_controller.status_activo, punto_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # operaciones
    if 'operation_x2' in request.POST.keys():
        operation = request.POST['operation_x2']
        if not operation in ['', 'modify_x']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'modify_x':
            if permisos.modificar:
                if punto_controller.puntos_almacenes(punto_id, request):
                    messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Puntos Almacenes!', 'description': 'Se guardaron los datos correctamente'})
                else:
                    # error al modificar
                    messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Puntos Almacenes!', 'description': punto_controller.error_operation})
            else:
                url = reverse('without_permission')
                return HttpResponseRedirect(url)

    # datos por defecto
    punto_actual = apps.get_model('configuraciones', 'Puntos').objects.select_related('sucursal_id').select_related('sucursal_id__ciudad_id').get(pk=punto_id)

    almacenes_lista = lista_controller.get_lista_almacenes(request.user, sucursal=punto_actual.sucursal_id)
    puntos_almacenes = apps.get_model('configuraciones', 'PuntosAlmacenes').objects.filter(status_id=punto_controller.status_activo, punto_id=punto_actual).order_by('punto_almacen_id')

    # almacenes ids
    almacenes_ids = ''
    for almacen in almacenes_lista:
        almacenes_ids += str(almacen.almacen_id) + '|'

    if len(almacenes_ids) > 0:
        almacenes_ids = almacenes_ids[0:len(almacenes_ids)-1]

    context = {
        'almacenes_lista': almacenes_lista,
        'puntos_almacenes': puntos_almacenes,
        'permisos': permisos,
        'url_main': '',
        'url_puntos': '',
        'punto_actual': punto_actual,
        'js_file': punto_controller.modulo_session,
        'autenticado': 'si',

        'almacenes_ids': almacenes_ids,

        'module_x': settings.MOD_PUNTOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'puntos_almacenes',
        'operation_x2': '',
        'operation_x3': '',

        'id': punto_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/puntos_almacenes.html', context)
