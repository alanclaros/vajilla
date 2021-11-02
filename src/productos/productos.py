import os
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
# settings de la app
from django.conf import settings
from django.apps import apps

# propios
from productos.models import Productos, ProductosImagenes, ProductosRelacionados

# para los usuarios
from utils.permissions import get_html_column, get_user_permission_operation, get_permissions_user

# clases por modulo
from controllers.productos.ProductosController import ProductosController
from controllers.ListasController import ListasController
from controllers.SystemController import SystemController

# imagenes
from django.core.files.base import ContentFile
from PIL import Image

from os import remove

from utils.validators import validate_number_int, validate_string


producto_controller = ProductosController()

# productos


@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PRODUCTOS, 'lista'), 'without_permission')
def productos_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_PRODUCTOS)
    # operaciones
    if 'operation_x' in request.POST.keys():
        try:
            operation = request.POST['operation_x']

            if not operation in ['', 'add', 'modify', 'delete', 'buscar_producto',
                                 'buscar_producto_relacionado', 'producto_relacionado', 'quitar_producto_relacionado',
                                 'copiar', 'imagenes', 'add_imagen', 'lista_imagenes', 'mostrar_imagen', 'eliminar_imagen']:
                return render(request, 'pages/without_permission.html', {})

            if operation == 'quitar_producto_relacionado':
                producto_id = validate_number_int('producto relacionado', request.POST['producto_relacionado_id'])

                if 'lista_relacionado' in request.session.keys():
                    lista_relacionado = request.session['lista_relacionado']
                else:
                    lista_relacionado = []

                indice = 0

                for li_co in lista_relacionado:
                    if int(li_co['producto_relacionado_id']) == int(producto_id):
                        lista_relacionado.pop(indice)
                    indice += 1

                # guardamos la session
                request.session['lista_relacionado'] = lista_relacionado
                request.session.modified = True

                context_relacionado = {
                    'productos_relacionados': lista_relacionado,
                    'autenticado': 'si',
                }
                return render(request, 'productos/productos_lista_relacionado.html', context_relacionado)

            if operation == 'producto_relacionado':
                producto_id = validate_number_int('producto id', request.POST['producto_id'])
                producto = validate_string('producto', request.POST['producto'], remove_specials='yes')

                if 'lista_relacionado' in request.session.keys():
                    lista_relacionado = request.session['lista_relacionado']
                else:
                    lista_relacionado = []

                existe = 'no'
                for li_co in lista_relacionado:
                    if li_co['producto_relacionado_id'] == producto_id:
                        existe = 'si'

                if existe == 'no':
                    dato_add = {}
                    dato_add['producto_relacionado_id'] = producto_id
                    dato_add['producto'] = producto
                    lista_relacionado.append(dato_add)

                # guardamos la session
                request.session['lista_relacionado'] = lista_relacionado
                request.session.modified = True

                context_relacionado = {
                    'productos_relacionados': lista_relacionado,
                    'autenticado': 'si',
                }
                return render(request, 'productos/productos_lista_relacionado.html', context_relacionado)

            if operation == 'buscar_producto_relacionado':
                linea = validate_string('linea', request.POST['linea'], remove_specials='yes', len_zero='yes')
                producto = validate_string('producto', request.POST['producto'], remove_specials='yes', len_zero='yes')
                codigo = validate_string('codigo', request.POST['codigo'], remove_specials='yes', len_zero='yes')
                operation_mandar = validate_string('operation_mandar', request.POST['operation_mandar'], remove_specials='yes')
                pid = validate_string('pid', request.POST['pid'], remove_specials='yes', len_zero='yes')

                busqueda_productos = producto_controller.buscar_producto(linea=linea, producto=producto, codigo=codigo, operation=operation_mandar, pid=pid)
                context_buscar = {
                    'productos': busqueda_productos,
                    'autenticado': 'si',
                }
                return render(request, 'productos/productos_buscar_relacionado.html', context_buscar)

            if operation == 'add':
                respuesta = productos_add(request)
                if not type(respuesta) == bool:
                    return respuesta

            if operation == 'modify' or operation == 'copiar':
                if operation == 'copiar':
                    request.session['copiar_producto'] = 'si'
                    request.session.modified = True

                respuesta = productos_modify(request, request.POST['id'])
                if not type(respuesta) == bool:
                    return respuesta

            if operation == 'delete':
                respuesta = productos_delete(request, request.POST['id'])
                if not type(respuesta) == bool:
                    return respuesta

            if operation == 'imagenes':
                # url = reverse('productos_imagenes', kwargs={'producto_id': int(request.POST['id'])})
                # return HttpResponseRedirect(url)
                respuesta = productos_images(request, request.POST['id'])
                if not type(respuesta) == bool:
                    return respuesta

            # adicion de imagen
            if operation == 'add_imagen':
                #print('add imagen')
                error = 0
                producto_id = request.POST['pid'].strip()
                posicion = int(request.POST['posicion'].strip())
                try:
                    if 'imagen1' in request.FILES.keys():
                        uploaded_filename = request.FILES['imagen1'].name

                        #full_filename = os.path.join(settings.STATIC_ROOT, 'media', 'productos', uploaded_filename)
                        system_controller = SystemController()
                        aux = system_controller.nombre_imagen('productos', uploaded_filename)

                        #full_filename = os.path.join(settings.STATIC_ROOT, 'media', 'productos', aux['nombre_archivo'])
                        #full_filename_thumb = os.path.join(settings.STATIC_ROOT, 'media', 'productos', aux['nombre_archivo_thumb'])
                        full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'productos', aux['nombre_archivo'])
                        full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'productos', aux['nombre_archivo_thumb'])

                        fout = open(full_filename, 'wb+')
                        file_content = ContentFile(request.FILES['imagen1'].read())
                        for chunk in file_content.chunks():
                            fout.write(chunk)
                        fout.close()

                        # creamos el thumb
                        imagen = Image.open(full_filename)
                        max_size = (settings.PRODUCTOS_THUMB_WIDTH, settings.PRODUCTOS_THUMB_HEIGHT)
                        imagen.thumbnail(max_size)
                        imagen.save(full_filename_thumb)

                        # registramos
                        producto = Productos.objects.get(pk=producto_id)
                        status_activo = apps.get_model('status', 'Status').objects.get(pk=producto_controller.activo)

                        producto_imagen = ProductosImagenes.objects.create(producto_id=producto, status_id=status_activo, posicion=posicion,
                                                                           imagen=aux['nombre_archivo'], imagen_thumb=aux['nombre_archivo_thumb'], created_at='now', updated_at='now')
                        producto_imagen.save()

                except Exception as ex:
                    error = 1
                    print('Error add imagen: ' + str(ex))

                producto = Productos.objects.get(pk=int(producto_id))
                productos_imagenes = ProductosImagenes.objects.filter(producto_id=producto, status_id=producto_controller.status_activo).order_by('posicion')
                context = {
                    'error': error,
                    'autenticado': 'si',
                    'productos_imagenes': productos_imagenes,
                }
                return render(request, 'productos/productos_imagenes_lista.html', context)

            if operation == 'lista_imagenes':
                # mostramos lista de productos
                producto_id = request.POST['pid'].strip()
                producto = Productos.objects.get(pk=int(producto_id))

                productos_imagenes = ProductosImagenes.objects.filter(producto_id=producto, status_id=producto_controller.status_activo).order_by('posicion')
                context = {
                    'productos_imagenes': productos_imagenes,
                    'autenticado': 'si',
                }
                return render(request, 'productos/productos_imagenes_lista.html', context)

            if operation == 'mostrar_imagen':
                producto_imagen = ProductosImagenes.objects.get(pk=int(request.POST['id']))
                context_img = {
                    'producto_imagen': producto_imagen,
                    'autenticado': 'si',
                }
                return render(request, 'productos/productos_imagenes_mostrar.html', context_img)

            if operation == 'eliminar_imagen':
                producto_imagen = ProductosImagenes.objects.get(pk=int(request.POST['id']))
                producto_id = producto_imagen.producto_id.producto_id
                # eliminamos los archivos
                full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'productos', producto_imagen.imagen)
                full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'productos', producto_imagen.imagen_thumb)
                try:
                    remove(full_filename)
                    remove(full_filename_thumb)
                except Exception as el:
                    print('no se pudo eliminar imagenes')

                producto_imagen.delete()

                producto = Productos.objects.get(pk=int(producto_id))
                status_activo = apps.get_model('status', 'Status').objects.get(pk=producto_controller.activo)
                productos_imagenes = ProductosImagenes.objects.filter(producto_id=producto, status_id=status_activo).order_by('posicion')
                context = {
                    'productos_imagenes': productos_imagenes,
                    'autenticado': 'si',
                }
                return render(request, 'productos/productos_imagenes_lista.html', context)

        except Exception as ex:
            return render(request, 'pages/internal_error.html', {'error': str(ex)})

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    productos_lista = producto_controller.index(request)
    #print('lista: ', productos_lista)
    productos_session = request.session[producto_controller.modulo_session]
    # print(zonas_session)
    context = {
        'productos': productos_lista,
        'session': productos_session,
        'permisos': permisos,

        'autenticado': 'si',
        'js_file': producto_controller.modulo_session,
        'columnas': producto_controller.columnas,

        'module_x': settings.MOD_PRODUCTOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'productos/productos.html', context)


# productos add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PRODUCTOS, 'adicionar'), 'without_permission')
def productos_add(request):
    # # url modulo
    lista_controller = ListasController()

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if producto_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Productos!', 'description': 'Se agrego el nuevo producto: '+request.POST['producto']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Productos!', 'description': producto_controller.error_operation})

    # lista de lineas
    lineas_lista = lista_controller.get_lista_lineas(request.user)

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(Productos, 'descripcion', request, None, 'producto', 'codigo', 'descripcion', 'stock_minimo', 'precio', 'precio_factura', 'costo_rotura')
    else:
        db_tags = get_html_column(Productos, 'descripcion', None, None, 'producto', 'codigo', 'descripcion', 'stock_minimo', 'precio', 'precio_factura', 'costo_rotura')

    if 'lista_relacionado' in request.session.keys():
        del request.session['lista_relacionado']

    context = {
        'url_main': '',
        'lineas_lista': lineas_lista,
        'db_tags': db_tags,
        'control_form': producto_controller.control_form,
        'js_file': producto_controller.modulo_session,

        'autenticado': 'si',

        'module_x': settings.MOD_PRODUCTOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }

    return render(request, 'productos/productos_form.html', context)


# productos modify
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PRODUCTOS, 'modificar'), 'without_permission')
def productos_modify(request, producto_id):

    producto_check = apps.get_model('productos', 'Productos').objects.filter(pk=producto_id)
    if not producto_check:
        return render(request, 'pages/without_permission.html', {})

    producto = Productos.objects.get(pk=producto_id)
    lista_controller = ListasController()

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        try:
            operation_copy = request.POST['operation_copy']

            if operation_copy == 'no':
                if producto_controller.save(request, type='modify'):
                    request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Productos!', 'description': 'Se modifico el producto: '+request.POST['producto']}
                    request.session.modified = True
                    return True
                else:
                    # error al modificar
                    existe_error = True
                    messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Productos!', 'description': producto_controller.error_operation})
            else:
                # copia de producto
                if producto_controller.save(request, type='add'):
                    request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Productos!', 'description': 'Se agrego el producto: '+request.POST['producto']}
                    request.session.modified = True
                    return True
                else:
                    # error al copiar
                    request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Productos!', 'description': 'No se puedo copiar el producto, ' + producto_controller.error_operation}
                    request.session.modified = True
                    return False

        except Exception as ex:
            return render(request, 'pages/internal_error.html', {'error': str(ex)})

            # restricciones de columna
    if existe_error:
        db_tags = get_html_column(Productos, 'descripcion', request, producto, 'producto', 'codigo', 'stock_minimo', 'precio', 'precio_factura', 'costo_rotura', 'descripcion')
    else:
        db_tags = get_html_column(Productos, 'descripcion', None, producto, 'producto', 'codigo', 'stock_minimo', 'precio', 'precio_factura', 'costo_rotura', 'descripcion')

    # lista de lineas
    lineas_lista = lista_controller.get_lista_lineas(request.user)

    # productos relacionados
    lista_pr = ProductosRelacionados.objects.select_related('producto_relacion_id').select_related('producto_relacion_id__linea_id').filter(
        status_id=producto_controller.status_activo, producto_id=producto).order_by('producto_relacion_id')
    lista_relacionado = []
    for pro_rel in lista_pr:
        dato_add = {}
        dato_add['producto_relacionado_id'] = str(pro_rel.producto_relacion_id.producto_id)
        dato_add['producto'] = pro_rel.producto_relacion_id.linea_id.linea + '-' + pro_rel.producto_relacion_id.producto
        lista_relacionado.append(dato_add)

    request.session['lista_relacionado'] = lista_relacionado
    request.session.modified = True

    # vemos si es de la opcion copiar
    if 'copiar_producto' in request.session.keys():
        del request.session['copiar_producto']
        request.session.modified = True
        operation_copy = 'si'
    else:
        operation_copy = 'no'

    context = {
        'url_main': '',
        'operation_copy': operation_copy,
        'producto': producto,

        'productos_relacionados': lista_relacionado,
        'lineas_lista': lineas_lista,
        'db_tags': db_tags,
        'control_form': producto_controller.control_form,
        'js_file': producto_controller.modulo_session,
        'status_active': producto_controller.activo,

        'autenticado': 'si',

        'module_x': settings.MOD_PRODUCTOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': producto_id,
        'id2': '',
        'id3': '',

    }

    return render(request, 'productos/productos_form.html', context)


# productos delete
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PRODUCTOS, 'eliminar'), 'without_permission')
def productos_delete(request, producto_id):
    # url modulo
    producto_check = apps.get_model('productos', 'Productos').objects.filter(pk=producto_id)
    if not producto_check:
        return render(request, 'pages/without_permission.html', {})

    producto = Productos.objects.get(pk=producto_id)

    # confirma eliminacion
    existe_error = False
    if 'delete_x' in request.POST.keys():
        if producto_controller.can_delete('producto_id', producto_id, **producto_controller.modelos_eliminar) and producto_controller.delete(producto_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Productos!', 'description': 'Se elimino el producto: '+request.POST['producto']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Productos!', 'description': producto_controller.error_operation})

    if producto_controller.can_delete('producto_id', producto_id, **producto_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Productos!', 'description': 'No puede eliminar este producto, ' + producto_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(Productos, '', request, producto, 'producto', 'codigo', 'stock_minimo', 'unidad')
    else:
        db_tags = get_html_column(Productos, '', None, producto, 'producto', 'codigo', 'stock_minimo', 'unidad')

    context = {
        'url_main': '',
        'producto': producto,
        'db_tags': db_tags,
        'control_form': producto_controller.control_form,
        'js_file': producto_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': producto_controller.error_operation,
        'autenticado': 'si',

        'module_x': settings.MOD_PRODUCTOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'delete',
        'operation_x2': '',
        'operation_x3': '',

        'id': producto_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'productos/productos_form_delete.html', context)


# productos images
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PRODUCTOS, 'modificar'), 'without_permission')
def productos_images(request, producto_id):

    producto_check = apps.get_model('productos', 'Productos').objects.filter(pk=producto_id)
    if not producto_check:
        return render(request, 'pages/without_permission.html', {})

    producto = Productos.objects.get(pk=producto_id)

    # guardamos
    existe_error = False
    if 'images_x' in request.POST.keys():
        if producto_controller.save_images(request, producto_id):
            messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Productos!', 'description': 'Se guardaron los datos de la imagen'})
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Productos!', 'description': producto_controller.error_operation})

    # lista de imagenes
    productos_imagenes = ProductosImagenes.objects.filter(producto_id=producto, status_id=producto_controller.status_activo).order_by('posicion')

    # producto = Productos.objects.select_related('linea_id').get(pk=producto_id)

    context = {
        'url_main': '',
        'producto': producto,
        'productos_imagenes': productos_imagenes,
        'control_form': producto_controller.control_form,
        'js_file': producto_controller.modulo_session,
        'status_active': producto_controller.activo,
        'pid': producto_id,
        'autenticado': 'si',

        'module_x': settings.MOD_PRODUCTOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'imagenes',
        'operation_x2': '',
        'operation_x3': '',

        'id': producto_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'productos/productos_imagenes.html', context)
