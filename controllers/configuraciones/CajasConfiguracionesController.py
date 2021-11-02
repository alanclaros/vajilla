
from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from configuraciones.models import Cajas
from utils.validators import validate_string, validate_number_int


class CajasConfiguracionesController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Cajas'
        self.modelo_id = 'caja_id'
        self.modelo_app = 'configuraciones'
        self.modulo_id = settings.MOD_PUNTOS

        # variables de session
        self.modulo_session = "cajas"
        self.columnas.append('tipo_moneda_id__codigo')
        self.columnas.append('caja')
        self.columnas.append('codigo')

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"
        self.variable_order_type_value = 'ASC'

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {}

        # control del formulario
        self.control_form = "txt|2|S|caja|Caja;"
        self.control_form += "txt|2|S|codigo|Codigo"

    def index(self, request, punto_id):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]

        # punto
        punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=punto_id)
        self.filtros_modulo['punto_id'] = punto

        # paginacion, paginas y definiendo el LIMIT *,*
        self.pagination()
        # asigamos la paginacion a la session
        request.session[self.modulo_session]['pages_list'] = self.pages_list

        # recuperamos los datos
        return self.get_list()

    def records_count(self):
        """cantidad de registros del modulo"""

        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        cantidad = modelo.objects.select_related('tipo_moneda_id').filter(**self.filtros_modulo).count()

        return cantidad

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
        retorno = modelo.objects.select_related('tipo_moneda_id').filter(**self.filtros_modulo).order_by(orden_enviar)[self.pages_limit_botton:self.pages_limit_top]

        return retorno

    def is_in_db(self, id, punto_id, nuevo_valor):
        """verificamos si existe en la base de datos"""
        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        filtros = {}
        filtros['status_id_id__in'] = [self.activo, self.inactivo]
        #filtros['tipo_moneda_id__in'] = [nuevo_valor]
        filtros['caja__iexact'] = nuevo_valor
        filtros['punto_id_id__in'] = [punto_id]
        if id:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        # si no existe
        if cantidad > 0:
            return True

        return False

    def save(self, request, punto_id, type='add'):
        """aniadimos nuevo punto"""
        try:
            tipo_moneda_id = validate_number_int('tipo moneda', request.POST['tipo_moneda'])
            caja_txt = validate_string('caja', request.POST['caja'])
            codigo_txt = validate_string('codigo', request.POST['codigo'])
            id = validate_number_int('id', request.POST['id2'], len_zero='yes')

            if not self.is_in_db(id, punto_id, caja_txt):
                # activo
                if 'activo' in request.POST.keys():
                    status_caja = self.status_activo
                else:
                    status_caja = self.status_inactivo

                # punto, tipo_moneda y usuario
                punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=int(punto_id))
                tipo_moneda = apps.get_model('configuraciones', 'TiposMonedas').objects.get(pk=tipo_moneda_id)
                usuario = request.user
                user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=usuario)

                if type == 'add':
                    caja = Cajas.objects.create(punto_id=punto, user_perfil_id=user_perfil, tipo_moneda_id=tipo_moneda, caja=caja_txt,
                                                codigo=codigo_txt, status_id=status_caja, created_at='now', updated_at='now')
                    caja.save()
                    self.error_operation = ""
                    return True

                if type == 'modify':
                    caja = Cajas.objects.get(pk=id)
                    caja.punto_id = punto
                    caja.tipo_moneda_id = tipo_moneda
                    caja.status_id = status_caja
                    caja.caja = caja_txt
                    caja.codigo = codigo_txt
                    caja.updated_at = 'now'
                    caja.save()
                    self.error_operation = ""
                    return True

                self.error_operation = 'Operation no valid'
                return False

            else:
                tipo_moneda = apps.get_model('configuraciones', 'TiposMonedas').objects.get(pk=tipo_moneda_id)
                self.error_operation = "Ya existe esta caja: " + tipo_moneda.codigo
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar la caja, " + str(ex)
            return False
