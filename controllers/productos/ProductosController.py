from decimal import Decimal
from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from productos.models import Productos, ProductosRelacionados, ProductosImagenes
from permisos.models import UsersPerfiles
from configuraciones.models import Puntos, Lineas
from status.models import Status

from django.db import transaction

# conexion directa a la base de datos
from django.db import connection

from utils.validators import validate_string, validate_number_int, validate_number_decimal

from controllers.SystemController import SystemController


class ProductosController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Productos'
        self.modelo_id = 'producto_id'
        self.modelo_app = 'productos'
        self.modulo_id = settings.MOD_PRODUCTOS

        # variables de session
        self.modulo_session = "productos"
        self.columnas.append('linea_id__linea')
        self.columnas.append('producto')
        self.columnas.append('codigo')

        self.variables_filtros.append('search_linea')
        self.variables_filtros.append('search_producto')
        self.variables_filtros.append('search_codigo')

        self.variables_filtros_defecto['search_linea'] = ''
        self.variables_filtros_defecto['search_producto'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'ventas': 'VentasDetalles'}

        # control del formulario
        self.control_form = "txt|2|S|producto|Producto;"
        self.control_form += "txt|2|S|codigo|Codigo;"
        self.control_form += "txt|1|S|precio|Precio;"
        self.control_form += "txt|1|S|precio_factura|Precio Factura;"
        self.control_form += "txt|1|S|costo_rotura|Costo Rotura;"
        self.control_form += "txt|1|S|stock_minimo|Stock Minimo"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]
        # linea
        if self.variables_filtros_values['search_linea'].strip() != "":
            self.filtros_modulo['linea_id__linea__icontains'] = self.variables_filtros_values['search_linea'].strip()
        # producto
        if self.variables_filtros_values['search_producto'].strip() != "":
            self.filtros_modulo['producto__icontains'] = self.variables_filtros_values['search_producto'].strip()
        # codigo
        if self.variables_filtros_values['search_codigo'].strip() != "":
            self.filtros_modulo['codigo__icontains'] = self.variables_filtros_values['search_codigo'].strip()

        # paginacion, paginas y definiendo el LIMIT *,*
        self.pagination()
        # asigamos la paginacion a la session
        request.session[self.modulo_session]['pages_list'] = self.pages_list

        # recuperamos los datos
        return self.get_list()

    def get_list(self):
        # orden
        orden_enviar = ''
        if self.variable_order_value != '':
            orden_enviar = self.variable_order_value
            if self.variable_order_type_value != '':
                if self.variable_order_type_value == 'DESC':
                    orden_enviar = '-' + orden_enviar
        # print(orden_enviar)

        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        retorno = modelo.objects.select_related('linea_id').filter(**self.filtros_modulo).order_by(orden_enviar)[self.pages_limit_botton:self.pages_limit_top]
        # for key, value in retorno.__dict__.items():
        #     print('key:', key, ' value:', value)

        return retorno

    def is_in_db(self, id, linea, nuevo_valor):
        """verificamos si existe en la base de datos"""
        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        filtros = {}
        filtros['status_id_id__in'] = [self.activo, self.inactivo]
        filtros['producto__iexact'] = nuevo_valor

        if id:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        #print('cantidad...: ', cantidad)
        # si no existe
        if cantidad > 0:
            return True

        return False

    def is_codigo_barras_db(self, id, codigo_barras):
        """verificando el codigo de barras"""

        # ahora sin control de codigo de barras
        # modelo = apps.get_model(self.modelo_app, self.modelo_name)
        # filtros = {}
        # filtros['status_id_id__in'] = [self.activo, self.inactivo]
        # filtros['codigo_barras__iexact'] = codigo_barras
        #
        # if id:
        #     cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        # else:
        #     cantidad = modelo.objects.filter(**filtros).count()
        #
        # # si no existe
        # if cantidad > 0:
        #     return True

        return False

    def save(self, request, type='add'):
        """aniadimos un nuevo producto"""
        try:
            linea_id = validate_number_int('linea', request.POST['linea'])
            producto_txt = validate_string('producto', request.POST['producto'], remove_specials='yes')
            codigo = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
            precio = validate_number_decimal('precio', request.POST['precio'])
            precio_factura = validate_number_decimal('precio_factura', request.POST['precio_factura'])
            costo_rotura = validate_number_decimal('costo_rotura', request.POST['costo_rotura'])
            stock_minimo = validate_number_int('stock minimo', request.POST['stock_minimo'])
            activo = 1 if 'activo' in request.POST.keys() else 0

            descripcion = validate_string('descripcion', request.POST['descripcion'], remove_specials='yes', len_zero='yes')
            id = validate_number_int('id', request.POST['id'], len_zero='yes')
            #print('producto id...', id)

            if not self.is_in_db(id, linea_id, producto_txt):

                # activo
                if activo == 1:
                    status_producto = self.status_activo
                else:
                    status_producto = self.status_inactivo

                # punto
                usuario = request.user
                user_perfil = UsersPerfiles.objects.get(user_id=usuario)
                linea = Lineas.objects.get(pk=linea_id)

                datos = {}
                datos['id'] = id
                datos['producto'] = producto_txt
                datos['codigo'] = codigo
                datos['precio'] = precio
                datos['precio_factura'] = precio_factura
                datos['costo_rotura'] = costo_rotura
                datos['linea_id'] = linea
                datos['stock_minimo'] = stock_minimo

                datos['descripcion'] = descripcion

                datos['created_at'] = 'now'
                datos['updated_at'] = 'now'
                datos['user_perfil_id'] = user_perfil
                datos['status_id'] = status_producto
                #datos['punto_id'] = punto

                # datos relacionados
                datos_relacionados = []

                if 'lista_relacionado' in request.session.keys():
                    lista_relacionado = request.session['lista_relacionado']
                    for relacionado in lista_relacionado:
                        dato_producto = {}
                        dato_producto['producto_id'] = relacionado['producto_relacionado_id']
                        datos_relacionados.append(dato_producto)

                #print('datos relacionado:', datos_relacionados)
                datos['datos_relacionados'] = datos_relacionados

                if self.save_db(type, **datos):
                    self.error_operation = ""
                    return True
                else:
                    return False

            else:
                self.error_operation = "Ya existe este producto: " + producto_txt
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar producto, " + str(ex)
            print('Error: ', str(ex))
            return False

    def save_db(self, type='add', **datos):
        """aniadimos a la base de datos"""
        try:

            if not self.is_in_db(datos['id'], datos['linea_id'].linea_id, datos['producto']):

                if type == 'add':

                    with transaction.atomic():
                        campos_add = {}
                        campos_add['producto'] = datos['producto']
                        campos_add['codigo'] = datos['codigo']
                        campos_add['precio'] = datos['precio']
                        campos_add['precio_factura'] = datos['precio_factura']
                        campos_add['costo_rotura'] = datos['costo_rotura']
                        campos_add['linea_id'] = datos['linea_id']
                        campos_add['stock_minimo'] = datos['stock_minimo']

                        campos_add['descripcion'] = datos['descripcion']

                        campos_add['created_at'] = datos['created_at']
                        campos_add['updated_at'] = datos['updated_at']
                        campos_add['user_perfil_id'] = datos['user_perfil_id']
                        campos_add['status_id'] = datos['status_id']

                        producto_add = Productos.objects.create(**campos_add)
                        producto_add.save()

                        # borramos antes de insertar productos relacionados
                        productos_relacionados_lista = ProductosRelacionados.objects.filter(producto_id=producto_add)
                        productos_relacionados_lista.delete()

                        for producto in datos['datos_relacionados']:
                            producto_relacion = Productos.objects.get(pk=producto['producto_id'])
                            producto_relacionado = ProductosRelacionados.objects.create(producto_id=producto_add, producto_relacion_id=producto_relacion,
                                                                                        status_id=datos['status_id'], created_at='now', updated_at='now')
                            producto_relacionado.save()

                        self.error_operation = ''
                        return True

                if type == 'modify':
                    with transaction.atomic():
                        campos_update = {}
                        campos_update['producto'] = datos['producto']
                        campos_update['codigo'] = datos['codigo']
                        campos_update['precio'] = datos['precio']
                        campos_update['precio_factura'] = datos['precio_factura']
                        campos_update['costo_rotura'] = datos['costo_rotura']
                        campos_update['linea_id'] = datos['linea_id']
                        campos_update['stock_minimo'] = datos['stock_minimo']

                        campos_update['descripcion'] = datos['descripcion']
                        campos_update['updated_at'] = datos['updated_at']
                        campos_update['status_id'] = datos['status_id']

                        producto_update = Productos.objects.filter(pk=datos['id'])
                        producto_update.update(**campos_update)

                        producto_actual = Productos.objects.get(pk=datos['id'])

                        # borramos antes de insertar productos relacionados
                        productos_relacionados_lista = ProductosRelacionados.objects.filter(producto_id=producto_actual)
                        productos_relacionados_lista.delete()

                        for producto in datos['datos_relacionados']:
                            producto_relacion = Productos.objects.get(pk=producto['producto_id'])
                            producto_relacionado = ProductosRelacionados.objects.create(producto_id=producto_actual, producto_relacion_id=producto_relacion,
                                                                                        status_id=datos['status_id'], created_at='now', updated_at='now')
                            producto_relacionado.save()

                        self.error_operation = ''
                        return True

                self.error_operation = 'operation no valid db'
                return False
            else:
                self.error_operation = "Ya existe este producto: " + datos['producto']
                return False

        except Exception as ex:
            self.error_operation = 'error de argumentos,' + str(ex)
            print('ERROR productos add, ' + str(ex))
            return False

    def buscar_producto(self, linea='', producto='', codigo='', operation='', pid=''):
        """busqueda de productos"""
        filtros = {}
        filtros['status_id__in'] = [self.activo]
        #filtros['es_combo'] = False

        if linea.strip() != '':
            filtros['linea_id__linea__icontains'] = linea
        if producto.strip() != '':
            filtros['producto__icontains'] = producto
        if codigo.strip() != '':
            filtros['codigo__icontains'] = codigo

        if operation == 'modify':
            productos_lista = Productos.objects.select_related('linea_id').filter(**filtros).exclude(pk=int(pid)).order_by('linea_id__linea', 'producto')[0:30]
        else:
            productos_lista = Productos.objects.select_related('linea_id').filter(**filtros).order_by('linea_id__linea', 'producto')[0:30]

        return productos_lista

    def save_images(self, request, producto_id):
        """guardamos las posiciones de las imagenes"""
        try:
            producto = Productos.objects.get(pk=producto_id)
            productos_imagenes = ProductosImagenes.objects.filter(producto_id=producto)

            for producto_imagen in productos_imagenes:
                aux = 'posicion_' + str(producto_imagen.producto_imagen_id)
                #print('aux: ', aux)
                if aux in request.POST.keys():
                    valor = 0 if request.POST[aux].strip() == '' else int(request.POST[aux].strip())
                    producto_imagen.posicion = valor
                    producto_imagen.save()

            return True

        except Exception as e:
            print('error guardar posicion imagen: ', str(e))
            self.error_operation = 'Error al guardar posiciones de imagen'
            return False

    def lista_productos(self, linea_id=0, punto_id=0):
        """lista de productos por linea seleccionada o todos"""
        datos_productos = []

        try:
            if linea_id == 0:
                sql_add = ''
            else:
                sql_add = f"AND l.linea_id='{linea_id}' "

            msql = f"SELECT l.linea, p.producto, p.codigo, p.precio, p.precio_factura, p.costo_rotura, p.producto_id "
            msql += f"FROM productos p, lineas l WHERE p.linea_id=l.linea_id AND l.status_id='{self.activo}' AND p.status_id='{self.activo}' "
            msql += sql_add
            msql += f"ORDER BY l.linea, p.producto "
            #print('msql ', msql)

            with connection.cursor() as cursor:
                cursor.execute(msql)
                rows = cursor.fetchall()
                for row in rows:
                    datos_productos.append({'linea': row[0], 'producto': row[1], 'codigo': row[2], 'precio': row[3], 'precio_factura': row[4], 'costo_rotura': row[5],
                                            'producto_id': row[6]})

            return datos_productos

        except Exception as e:
            print('error lista productos: ', str(e))
            self.error_operation = 'Error al recuperar lista productos'
            return False
