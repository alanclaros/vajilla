from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from utils.validators import validate_number_int, validate_string


class AlmacenesController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Almacenes'
        self.modelo_id = 'almacen_id'
        self.modelo_app = 'configuraciones'
        self.modulo_id = settings.MOD_ALMACENES

        # variables de session
        self.modulo_session = "almacenes"
        self.columnas.append('almacen')
        self.columnas.append('codigo')

        self.variables_filtros.append('search_almacen')
        self.variables_filtros.append('search_codigo')

        self.variables_filtros_defecto['search_almacen'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'configuraciones': 'PuntosAlmacenes'}

        # control del formulario
        self.control_form = "txt|2|S|almacen|Almacen;"
        self.control_form += "txt|2|S|codigo|Codigo"

    def index(self, request, sucursal_id):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]

        # sucursal
        sucursal = apps.get_model('configuraciones', 'Sucursales').objects.get(pk=sucursal_id)
        self.filtros_modulo['sucursal_id'] = sucursal
        # almacen
        if self.variables_filtros_values['search_almacen'].strip() != "":
            self.filtros_modulo['almacen__icontains'] = self.variables_filtros_values['search_almacen'].strip()

        # codigo
        if self.variables_filtros_values['search_codigo'].strip() != "":
            self.filtros_modulo['codigo__icontains'] = self.variables_filtros_values['search_codigo'].strip()

        # paginacion, paginas y definiendo el LIMIT *,*
        self.pagination()
        # asigamos la paginacion a la session
        request.session[self.modulo_session]['pages_list'] = self.pages_list

        # recuperamos los datos
        return self.get_lista()

    def records_count(self):
        """cantidad de registros del modulo"""
        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        cantidad = modelo.objects.select_related('sucursal_id').filter(**self.filtros_modulo).count()

        return cantidad

    def get_lista(self):
        # orden
        #print(self.variable_order_value, self.variable_order_type_value)
        orden_enviar = ''
        if self.variable_order_value != '':
            orden_enviar = self.variable_order_value
            if self.variable_order_type_value != '':
                if self.variable_order_type_value == 'DESC':
                    orden_enviar = '-' + orden_enviar
        # print(orden_enviar)

        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        retorno = modelo.objects.select_related('sucursal_id').filter(**self.filtros_modulo).order_by(orden_enviar)[self.pages_limit_botton:self.pages_limit_top]
        # for sucursal in retorno:
        #    # print(ciudad.__dict__)
        #    print(sucursal.ciudad_id.pais_id.__dict__)

        return retorno

    def is_in_db(self, id, sucursal_id, nuevo_valor):
        """verificamos si existe en la base de datos"""
        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        filtros = {}
        filtros['status_id_id__in'] = [self.activo, self.inactivo]
        filtros['almacen__in'] = [nuevo_valor]
        filtros['sucursal_id_id__in'] = [sucursal_id]
        if id:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        #print('cantidad', cantidad)
        # si no existe
        if cantidad > 0:
            return True

        return False

    def save(self, request, sucursal_id, type='add'):
        """
        add new almacen
        :param request: (object) request object
        :param sucursal_id: (object) sucursal owner
        :return: True if add else false
        """
        try:
            almacen_txt = validate_string('almacen', request.POST['almacen'], remove_specials='yes')
            codigo_txt = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
            id = validate_number_int('id', request.POST['id2'], len_zero='yes')
            # sucursal
            sucursal = apps.get_model('configuraciones', 'Sucursales').objects.get(pk=int(sucursal_id))

            if not self.is_in_db(id, sucursal_id, almacen_txt):
                # activo
                if 'activo' in request.POST.keys():
                    status_almacen = self.status_activo
                else:
                    status_almacen = self.status_inactivo

                if type == 'add':
                    almacen = apps.get_model('configuraciones', 'Almacenes').objects.create(
                        sucursal_id=sucursal, almacen=almacen_txt, codigo=codigo_txt,
                        status_id=status_almacen, created_at='now', updated_at='now')
                    almacen.save()
                    self.error_operation = ""
                    return True

                if type == 'modify':
                    almacen = apps.get_model('configuraciones', 'Almacenes').objects.get(pk=id)
                    # datos
                    almacen.sucursal_id = sucursal
                    almacen.status_id = status_almacen
                    almacen.almacen = almacen_txt
                    almacen.codigo = codigo_txt
                    almacen.updated_at = 'now'
                    almacen.save()
                    self.error_operation = ""
                    return True

                self.error_operation = 'Operacion no permitida'
                return False

            else:
                self.error_operation = "Ya existe este almacen: " + almacen_txt
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar el almacen, " + str(ex)
            return False
