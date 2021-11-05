from decimal import Decimal

from controllers.DefaultValues import DefaultValues
from django.apps import apps
from django.conf import settings


class PendientesController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Ventas'
        self.modelo_id = 'venta_id'
        self.modelo_app = 'ventas'
        self.modulo_id = settings.MOD_VENTAS

        # variables de session
        self.modulo_session = "pendientes"
        self.columnas.append('fecha_evento')
        self.columnas.append('apellidos')
        self.columnas.append('nombres')
        self.columnas.append('total')

        self.variables_filtros.append('search_numero_contrato')
        self.variables_filtros.append('search_apellidos')
        self.variables_filtros.append('search_nombres')
        self.variables_filtros.append('search_ci_nit')

        self.variables_filtros_defecto['search_numero_contrato'] = ''
        self.variables_filtros_defecto['search_apellidos'] = ''
        self.variables_filtros_defecto['search_nombres'] = ''
        self.variables_filtros_defecto['search_ci_nit'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"
        self.variable_order_type_value = 'DESC'

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {}

        # control del formulario
        self.control_form = ""

    def index(self, request):
        DefaultValues.index(self, request)

        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id__in'] = [self.status_venta, self.status_salida_almacen, self.status_vuelta_almacen]

        # numero_contrato
        if self.variables_filtros_values['search_numero_contrato'].strip() != "":
            self.filtros_modulo['numero_contrato'] = self.variables_filtros_values['search_numero_contrato'].strip()
        else:
            # apellidos
            if self.variables_filtros_values['search_apellidos'].strip() != "":
                self.filtros_modulo['apellidos_icontains'] = self.variables_filtros_values['search_apellidos'].strip()
            # nombres
            if self.variables_filtros_values['search_nombres'].strip() != "":
                self.filtros_modulo['nombres__icontains'] = self.variables_filtros_values['search_nombres'].strip()
            # ci nit
            if self.variables_filtros_values['search_ci_nit'].strip() != "":
                self.filtros_modulo['ci_nit__icontains'] = self.variables_filtros_values['search_ci_nit'].strip()

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
        retorno = modelo.objects.select_related('almacen_id').filter(**self.filtros_modulo).order_by(orden_enviar)[self.pages_limit_botton:self.pages_limit_top]

        return retorno

    def permission_operation(self, user_perfil, operation):
        """add ingreso almacen"""
        try:
            if user_perfil.perfil_id.perfil_id == settings.PERFIL_ADMIN:
                return True

            if user_perfil.perfil_id.perfil_id == settings.PERFIL_SUPERVISOR:
                return True

            if user_perfil.perfil_id.perfil_id == settings.PERFIL_ALMACEN:
                return True

            if user_perfil.perfil_id.perfil_id == settings.PERFIL_CAJERO:
                return True

            return False

        except Exception as ex:
            print('Error in permission operation, ', str(ex))
            return False
