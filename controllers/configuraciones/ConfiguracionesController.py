from django.conf import settings
from django.apps import apps

from controllers.DefaultValues import DefaultValues
# from configuraciones.models import Configuraciones
# from status.models import Status

from utils.validators import validate_number_int, validate_number_decimal, validate_string
from utils.dates_functions import get_date_to_db


class ConfiguracionesController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Configuraciones'
        self.modelo_id = 'configuracion_id'
        self.modelo_app = 'configuraciones'
        self.modulo_id = settings.MOD_CONFIGURACIONES_SISTEMA

        # variables de session
        self.modulo_session = "configuraciones"

        # paginas session
        self.variable_page = "ss_page"
        self.variable_page_defecto = "1"

        # control del formulario
        self.control_form = "txt|1|S|cant_per_page|Cantidad por Pagina;"
        self.control_form += "txt|1|S|minutos_antes_devolucion|Minutos antes de la devolucion;"
        self.control_form += "txt|1|S|minutos_despues_entrega|Minutos despues de la entrega"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()

        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        retorno = modelo.objects.get(pk=1)

        return retorno

    def add(self, request):
        """aniadimos"""
        pass

    def save(self, request, type='modify'):
        """modificamos"""
        try:
            cant_per_page = validate_number_int('cantidad pagina', request.POST['cant_per_page'])
            minutos_antes_devolucion = validate_number_int('minutos antes de la devolucion', request.POST['minutos_antes_devolucion'])
            minutos_despues_entrega = validate_number_int('minutos despues de la entrega', request.POST['minutos_despues_entrega'])
            usar_fecha_servidor = validate_string('usar_fecha_servidor', request.POST['usar_fecha_servidor'], remove_specials='yes')
            fecha_sistema = get_date_to_db(fecha=request.POST['fecha_sistema'].strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd')

            configuracion = apps.get_model('configuraciones', 'Configuraciones').objects.get(pk=1)
            configuracion.cant_per_page = cant_per_page
            configuracion.usar_fecha_servidor = usar_fecha_servidor
            configuracion.fecha_sistema = fecha_sistema
            configuracion.usar_fecha_servidor = usar_fecha_servidor
            configuracion.minutos_antes_devolucion = minutos_antes_devolucion
            configuracion.minutos_despues_entrega = minutos_despues_entrega
            configuracion.save()
            return True

        except Exception as ex:
            self.error_operation = "Error al actualizar los datos, " + str(ex)
            return False
