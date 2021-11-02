from permisos.models import UsersPerfiles
import app
from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from configuraciones.models import Puntos
# from status.models import Status
# from productos.models import PuntosPrecios

from decimal import Decimal
from utils.validators import validate_number_int, validate_string, validate_number_decimal

from controllers.ListasController import ListasController

# transacciones
from django.db import transaction


class PuntosController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Puntos'
        self.modelo_id = 'punto_id'
        self.modelo_app = 'configuraciones'
        self.modulo_id = settings.MOD_PUNTOS

        # variables de session
        self.modulo_session = "puntos"
        self.columnas.append('sucursal_id__sucursal')
        self.columnas.append('punto')
        self.columnas.append('codigo')

        self.variables_filtros.append('search_sucursal')
        self.variables_filtros.append('search_punto')

        self.variables_filtros_defecto['search_sucursal'] = ''
        self.variables_filtros_defecto['search_punto'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'configuraciones': 'Cajas', 'inventarios': 'Registros', 'ventas': 'Ventas'}

        # control del formulario
        self.control_form = "txt|2|S|punto|Punto;"
        self.control_form += "txt|2|S|codigo|Codigo"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]
        # sucursal
        if self.variables_filtros_values['search_sucursal'].strip() != "":
            self.filtros_modulo['sucursal_id__sucursal__icontains'] = self.variables_filtros_values['search_sucursal'].strip()
        # punto
        if self.variables_filtros_values['search_punto'].strip() != "":
            self.filtros_modulo['punto__icontains'] = self.variables_filtros_values['search_punto'].strip()

        # paginacion, paginas y definiendo el LIMIT *,*
        self.pagination()
        # asigamos la paginacion a la session
        request.session[self.modulo_session]['pages_list'] = self.pages_list

        # recuperamos los datos
        return self.get_list()

    def records_count(self):
        """cantidad de registros del modulo"""

        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        cantidad = modelo.objects.select_related('sucursal_id').select_related('sucursal_id__ciudad_id').filter(**self.filtros_modulo).count()

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
        retorno = modelo.objects.select_related('sucursal_id').select_related('sucursal_id__ciudad_id').filter(**self.filtros_modulo).order_by(orden_enviar)[self.pages_limit_botton:self.pages_limit_top]
        # for sucursal in retorno:
        #    # print(ciudad.__dict__)
        #    print(sucursal.ciudad_id.pais_id.__dict__)

        return retorno

    def is_in_db(self, id, sucursal_id, nuevo_valor):
        """verificamos si existe en la base de datos"""
        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        filtros = {}
        filtros['status_id_id__in'] = [self.activo, self.inactivo]
        filtros['punto__iexact'] = nuevo_valor
        filtros['sucursal_id_id__in'] = [sucursal_id]
        if id:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        if cantidad > 0:
            return True

        return False

    def save(self, request, type='add'):
        """aniadimos nuevo punto"""
        try:
            sucursal_id = validate_number_int('sucursal', request.POST['sucursal'])
            punto_txt = validate_string('punto', request.POST['punto'])
            codigo_txt = validate_string('codigo', request.POST['codigo'])
            id = validate_number_int('id', request.POST['id'], len_zero='yes')

            if not self.is_in_db(id, sucursal_id, punto_txt):
                # activo
                if 'activo' in request.POST.keys():
                    status_punto = self.status_activo
                else:
                    status_punto = self.status_inactivo

                # sucursal y usuario
                sucursal = apps.get_model('configuraciones', 'Sucursales').objects.get(pk=sucursal_id)
                usuario = request.user
                user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=usuario)

                if type == 'add':
                    punto = Puntos.objects.create(sucursal_id=sucursal, user_perfil_id=user_perfil, punto=punto_txt,
                                                  codigo=codigo_txt, impresora_reportes='', status_id=status_punto, created_at='now', updated_at='now')
                    punto.save()
                    self.error_operation = ""
                    return True

                if type == 'modify':
                    punto = Puntos.objects.get(pk=id)
                    # datos
                    punto.sucursal_id = sucursal
                    punto.status_id = status_punto
                    punto.punto = punto_txt
                    punto.codigo = codigo_txt
                    punto.updated_at = 'now'
                    punto.save()
                    self.error_operation = ""
                    return True

                self.error_operation = 'Operation no valid'
                return False

            else:
                self.error_operation = "Ya existe este punto: " + punto_txt
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar el punto, " + str(ex)
            return False

    def puntos_almacenes(self, punto_id, request):
        """puntos almacenes"""
        try:
            lista_controller = ListasController()

            with transaction.atomic():
                # lista de almacenes
                punto = Puntos.objects.get(pk=punto_id)
                lista_almacenes = lista_controller.get_lista_almacenes(request.user, punto.sucursal_id)

                # borramos antes de insertar
                puntos_almacenes = apps.get_model('configuraciones', 'PuntosAlmacenes').objects.filter(punto_id=punto)
                puntos_almacenes.delete()

                for almacen in lista_almacenes:
                    id_aux = 'almacen_' + str(almacen.almacen_id)
                    if id_aux in request.POST.keys():
                        punto_almacen = apps.get_model('configuraciones', 'PuntosAlmacenes').objects.create(status_id=self.status_activo, punto_id=punto,
                                                                                                            almacen_id=almacen, created_at='now', updated_at='now')
                        punto_almacen.save()

                self.error_operation = ""
                return True

        except Exception as ex:
            print('ERROR, puntos almacenes: ' + str(ex))
            self.error_operation = "Error al actualizar los puntos almacenes, " + str(ex)
            return False
