from django.apps import apps
from django.db.models import Max
from django.conf import settings
from utils.permissions import get_system_settings
from controllers.SystemController import SystemController


class DefaultValues(object):
    """
    Session for each module in the system
    """

    def __init__(self):
        # estados
        self.activo, self._status_activo = int(settings.STATUS_ACTIVO), None
        self.inactivo, self._status_inactivo = int(settings.STATUS_INACTIVO), None
        self.eliminado, self._status_eliminado = int(settings.STATUS_ELIMINADO), None
        self.anulado, self._status_anulado = int(settings.STATUS_ANULADO), None
        # estados de caja
        self.apertura, self._status_apertura = int(settings.STATUS_APERTURA), None
        self.apertura_recibe, self._status_apertura_recibe = int(settings.STATUS_APERTURA_RECIBE), None
        self.cierre, self._status_cierre = int(settings.STATUS_CIERRE), None
        self.cierre_recibe, self._status_cierre_recibe = int(settings.STATUS_CIERRE_RECIBE), None
        self.no_aperturado, self._status_no_aperturado = int(settings.STATUS_NO_APERTURADO), None
        # MOVIMIENTO CAJA
        self.movimiento_caja, self._status_movimiento_caja = int(settings.STATUS_MOVIMIENTO_CAJA), None
        self.movimiento_caja_recibe, self._status_movimiento_caja_recibe = int(settings.STATUS_MOVIMIENTO_CAJA_RECIBE), None
        # ventas
        self.preventa, self._status_preventa = int(settings.STATUS_PREVENTA), None
        self.venta, self._status_venta = int(settings.STATUS_VENTA), None
        self.salida_almacen, self._status_salida_almacen = int(settings.STATUS_SALIDA_ALMACEN), None
        self.vuelta_almacen, self._status_vuelta_almacen = int(settings.STATUS_VUELTA_ALMACEN), None
        self.finalizado, self._status_finalizado = int(settings.STATUS_FINALIZADO), None

        # perfil supervisor y admin
        self.perfil_admin = int(settings.PERFIL_ADMIN)
        self.perfil_supervisor = int(settings.PERFIL_SUPERVISOR)
        self.perfil_cajero = int(settings.PERFIL_CAJERO)
        self.perfil_almacen = int(settings.PERFIL_ALMACEN)

        # propiedades
        self.modelo_name = 'unknow'
        self.modelo_id = 'unknow'
        self.modelo_app = 'unknow'
        self.modulo_id = 0
        self.module_id_session = 'module_' + str(self.modulo_id)

        # filtros para el modulo
        self.filtros_modulo = {}

        # paginacion
        self.pages_list = []
        self.pages_limit_botton = 0
        self.pages_limit_top = 0

        # control del formulario
        self.control_form = ""

        # error en las operaciones
        self.error_operation = ""

        # tablas que se deben verificar para eliminar
        self.modelos_eliminar = {}

        # sesiones
        self.modulo_session = "unknow"

        # nombre variables filtros para la busqueda
        self.variables_filtros = []
        self.variables_filtros_defecto = {}
        self.variables_filtros_values = {}

        # nombre variable pagina actual
        self.variable_page, self.variable_page_defecto, self.variable_page_val = '', 1, 1

        # nombre de las variables de orden
        self.variable_order, self.variable_order_value = "", ""
        self.variable_order_type, self.variable_order_type_value = "", ""

        # columnas para el ordenamiento
        self.columnas = []

        # session de orden
        self.order_field = ""
        self.order_type = ""
        self.order_field_value = ""
        self.order_type_value = ""

    @property
    def status_activo(self):
        if self._status_activo is None:
            self._status_activo = apps.get_model('status', 'Status').objects.get(pk=self.activo)

        return self._status_activo

    @property
    def status_inactivo(self):
        if self._status_inactivo is None:
            self._status_inactivo = apps.get_model('status', 'Status').objects.get(pk=self.inactivo)

        return self._status_inactivo

    @property
    def status_eliminado(self):
        if self._status_eliminado is None:
            self._status_eliminado = apps.get_model('status', 'Status').objects.get(pk=self.eliminado)

        return self._status_eliminado

    @property
    def status_anulado(self):
        if self._status_anulado is None:
            self._status_anulado = apps.get_model('status', 'Status').objects.get(pk=self.anulado)

        return self._status_anulado

    @property
    def status_apertura(self):
        if self._status_apertura is None:
            self._status_apertura = apps.get_model('status', 'Status').objects.get(pk=self.apertura)

        return self._status_apertura

    @property
    def status_apertura_recibe(self):
        if self._status_apertura_recibe is None:
            self._status_apertura_recibe = apps.get_model('status', 'Status').objects.get(pk=self.apertura_recibe)

        return self._status_apertura_recibe

    @property
    def status_cierre(self):
        if self._status_cierre is None:
            self._status_cierre = apps.get_model('status', 'Status').objects.get(pk=self.cierre)

        return self._status_cierre

    @property
    def status_cierre_recibe(self):
        if self._status_cierre_recibe is None:
            self._status_cierre_recibe = apps.get_model('status', 'Status').objects.get(pk=self.cierre_recibe)

        return self._status_cierre_recibe

    @property
    def status_no_aperturado(self):
        if self._status_no_aperturado is None:
            self._status_no_aperturado = apps.get_model('status', 'Status').objects.get(pk=self.no_aperturado)

        return self._status_no_aperturado

    @property
    def status_movimiento_caja(self):
        if self._status_movimiento_caja is None:
            self._status_movimiento_caja = apps.get_model('status', 'Status').objects.get(pk=self.movimiento_caja)

        return self._status_movimiento_caja

    @property
    def status_movimiento_caja_recibe(self):
        if self._status_movimiento_caja_recibe is None:
            self._status_movimiento_caja_recibe = apps.get_model('status', 'Status').objects.get(pk=self.movimiento_caja_recibe)

        return self._status_movimiento_caja_recibe

    @property
    def status_preventa(self):
        if self._status_preventa is None:
            self._status_preventa = apps.get_model('status', 'Status').objects.get(pk=self.preventa)

        return self._status_preventa

    @property
    def status_venta(self):
        if self._status_venta is None:
            self._status_venta = apps.get_model('status', 'Status').objects.get(pk=self.venta)

        return self._status_venta

    @property
    def status_salida_almacen(self):
        if self._status_salida_almacen is None:
            self._status_salida_almacen = apps.get_model('status', 'Status').objects.get(pk=self.salida_almacen)

        return self._status_salida_almacen

    @property
    def status_vuelta_almacen(self):
        if self._status_vuelta_almacen is None:
            self._status_vuelta_almacen = apps.get_model('status', 'Status').objects.get(pk=self.vuelta_almacen)

        return self._status_vuelta_almacen

    @property
    def status_finalizado(self):
        if self._status_finalizado is None:
            self._status_finalizado = apps.get_model('status', 'Status').objects.get(pk=self.finalizado)

        return self._status_finalizado

    def get_max_id(self, *args):
        """return max id table"""
        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        max_id = modelo.objects.all().aggregate(Max(self.modelo_id))
        valor = list(max_id.values())[0]
        # print('max_id:', valor)
        if valor:
            valor += 1
        else:
            valor = 1

        return valor

    def records_count(self):
        """cantidad de registros del modulo"""
        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        cantidad = modelo.objects.filter(**self.filtros_modulo).count()

        return cantidad

    def index(self, request):
        """inicializando variables de session del modulo"""

        # varibles de session sin iniciar
        if not self.modulo_session in request.session.keys():
            request.session[self.modulo_session] = {}
            for val in self.variables_filtros:
                request.session[self.modulo_session][val] = self.variables_filtros_defecto[val]

            # pagina
            request.session[self.modulo_session][self.variable_page] = self.variable_page_defecto
            request.session[self.modulo_session]['pages_list'] = self.pages_list
            request.session[self.modulo_session]['variable_page'] = self.variable_page

            # order nombres variables
            request.session[self.modulo_session]['variable_order'] = self.variable_order
            request.session[self.modulo_session]['variable_order_type'] = self.variable_order_type
            # order
            request.session[self.modulo_session][self.variable_order] = self.variable_order_value
            if self.variable_order_type_value == '':
                self.variable_order_type_value = 'ASC'
            request.session[self.modulo_session][self.variable_order_type] = self.variable_order_type_value

        # si realiza alguna busqueda
        if 'search_button_x' in request.POST.keys():
            for val in self.variables_filtros:
                if val in request.POST.keys():
                    request.session[self.modulo_session][val] = request.POST[val]
                else:
                    request.session[self.modulo_session][val] = self.variable_negativo
            # pagina
            request.session[self.modulo_session][self.variable_page] = self.variable_page_defecto

        # si seleccionana una pagina
        if self.variable_page in request.POST.keys():
            request.session[self.modulo_session][self.variable_page] = int(request.POST[self.variable_page])

        # asignamos los valores por defecto o los valores seleccionados
        self.variables_filtros_values.clear()
        for val in self.variables_filtros:
            self.variables_filtros_values[val] = request.session[self.modulo_session][val]

        # pagina
        self.variable_page_val = request.session[self.modulo_session][self.variable_page]

        # order request
        if self.variable_order in request.POST.keys():
            request.session[self.modulo_session][self.variable_order] = request.POST[self.variable_order]
            request.session[self.modulo_session][self.variable_order_type] = request.POST[self.variable_order_type]

        # datos del orden
        self.variable_order_value = request.session[self.modulo_session][self.variable_order]
        self.variable_order_type_value = request.session[self.modulo_session][self.variable_order_type]

        # importante establecer que la session se modifico para cuando se vuelva al modulo mantenga los datos
        request.session.modified = True

    def pagination(self):
        settings_sistema = get_system_settings()
        cant_per_page = settings_sistema['cant_per_page']
        self.pages_list = []
        cant_total = self.records_count()
        j = 1
        i = 0
        while i < cant_total:
            self.pages_list.append(j)
            i = i + cant_per_page
            j += 1
            if j > 15:
                break

        self.pages_limit_botton = (int(self.variable_page_val) - 1) * cant_per_page
        self.pages_limit_top = self.pages_limit_botton + cant_per_page

    def get_list(self):
        # orden
        orden_enviar = ''
        if self.variable_order_value != '':
            orden_enviar = self.variable_order_value
            if self.variable_order_type_value != '':
                if self.variable_order_type_value == 'DESC':
                    orden_enviar = '-' + orden_enviar

        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        retorno = modelo.objects.filter(**self.filtros_modulo).order_by(orden_enviar)[self.pages_limit_botton:self.pages_limit_top]

        return retorno

    def save(self, request, type='add'):
        """agregar un elemento al modulo"""
        pass

    def save_db(self, **datos):
        """agregando en la base de datos"""
        pass

    def delete(self, id):
        # return True
        status_delete = apps.get_model('status', 'Status').objects.get(pk=self.eliminado)

        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        objeto = modelo.objects.get(pk=id)
        objeto.status_id = status_delete
        objeto.deleted_at = 'now'
        objeto.save()

        return True

    def can_delete(self, nombre_campo, id_valor, **app_modelo):
        """verificando si se puede eliminar la tabla"""
        # print('campo:', nombre_campo)
        # print('id:', id_valor)
        # print('datos:', app_modelo)
        system_controller = SystemController()

        for app, modelo_eliminar in app_modelo.items():
            if system_controller.model_exits(modelo_eliminar):
                modelo = apps.get_model(app, modelo_eliminar)
                cantidad = modelo.objects.filter(**{nombre_campo: id_valor}).exclude(pk=self.eliminado).count()
                if cantidad > 0:
                    self.error_operation = 'Tiene registros en el modulo ' + modelo_eliminar
                    return False

        return True

    def is_in_db(self, id, nuevo_valor):
        """verificamos si existe el nuevo valor en la base de datos"""
        """id-> en caso que se este modificando"""
        """nuevo_valor-> columna de la base de datos"""
        pass

    def permission_add(self, user_perfil, module, id):
        """permission to add record acordly user_perfil, module and id"""
        pass

    def permission_modify(self, user_perfil, module, id):
        """permission to modify record acordly user_perfil, module and id"""
        pass

    def permission_delete(self, user_perfil, module, id):
        """permission to delete record acordly user_perfil, module and id"""
        pass

    def permission_nullify(self, user_perfil, module, id):
        """permission to nullify record acordly user_perfil, module and id"""
        pass

    def permission_print(self, user_perfil, module, id):
        """permission to print record acordly user_perfil, module and id"""
        pass
