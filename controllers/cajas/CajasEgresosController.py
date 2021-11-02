from django.conf import settings
from django.apps import apps

from utils.dates_functions import get_date_to_db, get_date_show, get_date_system, get_seconds_date1_sub_date2, add_days_datetime
from controllers.DefaultValues import DefaultValues

from configuraciones.models import Cajas, Puntos
from permisos.models import UsersPerfiles
from cajas.models import CajasEgresos

from utils.validators import validate_string, validate_number_decimal, validate_number_int
from controllers.cajas.CajasController import CajasController

# transacciones
from django.db import transaction


class CajasEgresosController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)

        self.modelo_name = 'CajasEgresos'
        self.modelo_id = 'caja_egreso_id'
        self.modelo_app = 'cajas'
        self.modulo_id = settings.MOD_CAJAS_EGRESOS

        # variables de session
        self.modulo_session = "cajas_egresos"
        self.columnas.append('fecha')
        self.columnas.append('concepto')
        self.columnas.append('monto')

        self.variables_filtros.append('search_fecha_ini')
        self.variables_filtros.append('search_fecha_fin')
        self.variables_filtros.append('search_caja')
        self.variables_filtros.append('search_concepto')

        fecha_actual = get_date_system()
        fecha_inicio = add_days_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd', dias=0, formato='dd-MMM-yyyy')
        fecha_fin = get_date_show(fecha=fecha_actual, formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')

        self.variables_filtros_defecto['search_fecha_ini'] = fecha_inicio
        self.variables_filtros_defecto['search_fecha_fin'] = fecha_fin
        self.variables_filtros_defecto['search_caja'] = '0'
        self.variables_filtros_defecto['search_concepto'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"
        # orden descendente por defecto
        self.variable_order_type_value = 'DESC'

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {}

        # control del formulario
        self.control_form = "txt|2|S|fecha|Fecha"
        self.control_form += ";txt|2|S|concepto|Concepto"
        self.control_form += ";txt|1|S|monto|Monto"
        self.control_form += ";cbo|0|S|caja|Caja"

    def index(self, request):
        DefaultValues.index(self, request)

        # ultimo acceso
        if 'last_access' in request.session[self.modulo_session].keys():
            # restamos
            resta = abs(get_seconds_date1_sub_date2(fecha1=get_date_system(time='si'), formato1='yyyy-mm-dd HH:ii:ss', fecha2=request.session[self.modulo_session]['last_access'], formato2='yyyy-mm-dd HH:ii:ss'))
            #print('resta:', resta)
            if resta > 14400:  # 4 horas (4x60x60)
                # print('modificando')
                fecha_actual = get_date_system()
                fecha_inicio = add_days_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd', dias=0, formato='dd-MMM-yyyy')
                fecha_fin = get_date_show(fecha=fecha_actual, formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')

                self.variables_filtros_values['search_fecha_ini'] = fecha_inicio
                self.variables_filtros_defecto['search_fecha_ini'] = fecha_inicio
                self.variables_filtros_values['search_fecha_fin'] = fecha_fin
                self.variables_filtros_defecto['search_fecha_fin'] = fecha_fin

                # orden por defecto
                self.variable_order_value = self.columnas[0]
                self.variable_order_type_value = 'DESC'
                request.session[self.modulo_session][self.variable_order] = self.variable_order_value
                request.session[self.modulo_session][self.variable_order_type] = self.variable_order_type_value

                # session
                request.session[self.modulo_session]['search_fecha_ini'] = self.variables_filtros_defecto['search_fecha_ini']
                request.session[self.modulo_session]['search_fecha_fin'] = self.variables_filtros_defecto['search_fecha_fin']
                request.session.modified = True

            #print('variable:', self.variable_val)
            # actualizamos a la fecha actual
            request.session[self.modulo_session]['last_access'] = get_date_system(time='si')
            request.session.modified = True
        else:
            request.session[self.modulo_session]['last_access'] = get_date_system(time='si')
            request.session.modified = True

        # filtros del modulo
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.anulado]
        # punto

        usuario_perfil = UsersPerfiles.objects.get(user_id=request.user)
        punto_check = Puntos.objects.get(pk=usuario_perfil.punto_id)
        # administradores y supervisores pueden ver de la sucursal
        if usuario_perfil.perfil_id.perfil_id == self.perfil_admin or usuario_perfil.perfil_id.perfil_id == self.perfil_supervisor:
            self.filtros_modulo['punto_id__sucursal_id'] = punto_check.sucursal_id
        else:
            # usuario comun
            self.filtros_modulo['punto_id'] = usuario_perfil.punto_id

        # fechas
        if self.variables_filtros_values['search_fecha_ini'].strip() != '' and self.variables_filtros_values['search_fecha_fin'].strip() != '':
            self.filtros_modulo['fecha__gte'] = get_date_to_db(fecha=self.variables_filtros_values['search_fecha_ini'].strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo='00:00:00')
            self.filtros_modulo['fecha__lte'] = get_date_to_db(fecha=self.variables_filtros_values['search_fecha_fin'].strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo='23:59:59')
        # caja
        if self.variables_filtros_values['search_caja'].strip() != '0':
            self.filtros_modulo['caja_id_id'] = self.variables_filtros_values['search_caja'].strip()
        # concepto
        if self.variables_filtros_values['search_concepto'].strip() != "":
            self.filtros_modulo['concepto__icontains'] = self.variables_filtros_values['search_concepto'].strip()

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
        retorno = modelo.objects.select_related('caja_id').filter(**self.filtros_modulo).order_by(orden_enviar)[self.pages_limit_botton:self.pages_limit_top]
        # for sucursal in retorno:
        #    # print(ciudad.__dict__)
        #    print(sucursal.ciudad_id.pais_id.__dict__)

        return retorno

    def add(self, request):
        """aniadimos una nuevo registro"""
        try:
            # estado
            status_ce = self.status_activo
            caja_id = validate_number_int('caja', request.POST['caja'])
            concepto = validate_string('concepto', request.POST['concepto'], remove_specials='yes')
            monto = validate_number_decimal('monto', request.POST['monto'])
            fecha = validate_string('fecha', request.POST['fecha'])

            # caja, punto y usuario
            caja = Cajas.objects.get(pk=caja_id)
            punto = Puntos.objects.get(pk=caja.punto_id.punto_id)
            #usuario = request.user

            perfil_user = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
            # if perfil_user.caja_id != caja.caja_id:
            #     self.error_operation = 'Solo puede adicionar egresos en su caja'
            #     raise ValueError('Solo puede adicionar egresos en su caja')

            datos = {}
            datos['caja_id'] = caja
            datos['punto_id'] = punto
            datos['user_perfil_id'] = perfil_user
            datos['status_id'] = status_ce
            datos['fecha'] = get_date_to_db(fecha=fecha, formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss')
            datos['concepto'] = concepto
            datos['monto'] = monto
            datos['created_at'] = 'now'
            datos['updated_at'] = 'now'

            if self.add_db(**datos):
                self.error_operation = ""
                return True
            else:
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar el egreso de caja, " + str(ex)
            return False

    def add_db(self, **datos):
        """aniadimos a la base de datos"""
        try:
            with transaction.atomic():
                perfil_user = datos['user_perfil_id']
                if perfil_user.caja_id != datos['caja_id'].caja_id:
                    self.error_operation = 'Solo puede adicionar egresos en su caja'
                    return False

                caja_controller = CajasController()
                #print('caja...: ', datos['caja_id'])
                #print('la fecha...: ', datos['fecha'])
                saldo_dia = caja_controller.day_balance(fecha=datos['fecha'], Cajas=datos['caja_id'], formato_ori='yyyy-mm-dd')
                #saldo_dia = caja_controller.day_balance(fecha='2021-01-01', Cajas=datos['caja_id'], formato_ori='yyyy-mm-dd')
                saldo_caja = saldo_dia[datos['caja_id'].caja_id]
                if saldo_caja == '/N':
                    self.error_operation = 'No tiene saldo en esta caja'
                    return False

                if datos['monto'] > saldo_caja:
                    self.error_operation = 'El egreso no debe pasar de: ' + str(saldo_caja) + " Bs."
                    return False
                # return False

                # print(datos)
                campos_add = {}
                # campos fijos
                campos_add['caja_id'] = datos['caja_id']
                campos_add['punto_id'] = datos['punto_id']
                campos_add['user_perfil_id'] = datos['user_perfil_id']
                campos_add['status_id'] = datos['status_id']
                campos_add['fecha'] = datos['fecha']
                campos_add['concepto'] = datos['concepto']
                campos_add['monto'] = datos['monto']
                campos_add['created_at'] = datos['created_at']
                campos_add['updated_at'] = datos['updated_at']

                # campos opcionales
                if 'caja_movimiento_id' in datos.keys():
                    campos_add['caja_movimiento_id'] = datos['caja_movimiento_id']

                if 'venta_id' in datos.keys():
                    campos_add['venta_id'] = datos['venta_id']

                # registramos
                ce_add = CajasEgresos.objects.create(**campos_add)
                ce_add.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = "Error de argumentos: " + str(ex)
            print('ERROR, egreso caja add_db: ' + str(ex))
            return False

    def delete(self, request, id):
        # verificamos que llene el motivo
        try:
            motivo_anula = validate_string('motivo anula', request.POST['motivo_anula'])

            if not self.can_delete('caja_egreso_id', id, **self.modelos_eliminar):
                return False

            status_delete = self.status_anulado
            user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)

            campos_update = {}
            campos_update['status_id'] = status_delete
            campos_update['deleted_at'] = 'now'
            campos_update['user_perfil_id_anula'] = user_perfil
            campos_update['motivo_anula'] = motivo_anula

            if self.delete_db(id, **campos_update):
                self.error_operation = ""
                return True
            else:
                return False

        except Exception as ex:
            self.error_operation = 'error al anular, ' + str(ex)
            return False

    def delete_db(self, caja_egreso_id, **datos):
        """anulamos de la base de datos"""
        try:
            with transaction.atomic():
                user_perfil = datos['user_perfil_id_anula']
                caja_egreso = CajasEgresos.objects.get(pk=caja_egreso_id)

                puede_anular = False
                if user_perfil.perfil_id.perfil_id == settings.PERFIL_ADMIN:
                    #print('perfil admin....')
                    puede_anular = True

                if user_perfil.perfil_id.perfil_id == settings.PERFIL_SUPERVISOR:
                    punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)
                    filtro_supervisor = {}
                    filtro_supervisor['punto_id__sucursal_id'] = punto.sucursal_id
                    filtro_supervisor['status_id'] = self.status_activo
                    cajas_punto = apps.get_model('configuraciones', 'Cajas').objects.filter(**filtro_supervisor)
                    #print('cajas punto: ', cajas_punto)
                    for caja_punto in cajas_punto:
                        if caja_egreso.caja_id == caja_punto:
                            puede_anular = True
                            #print('con permiso...')

                if user_perfil.perfil_id.perfil_id == settings.PERFIL_CAJERO:
                    if caja_egreso.caja_id.caja_id == user_perfil.caja_id:
                        puede_anular = True
                        #print('cajero puee anular...')

                #puede_anular = False
                if not puede_anular:
                    self.error_operation = 'Solo puede anular ingresos de su caja o sucursal'
                    return False

                campos_update = {}
                # campos fijos
                campos_update['user_perfil_id_anula'] = user_perfil.user_perfil_id
                campos_update['status_id'] = datos['status_id']
                campos_update['motivo_anula'] = datos['motivo_anula']
                campos_update['deleted_at'] = datos['deleted_at']

                # registramos
                ce_update = CajasEgresos.objects.filter(pk=caja_egreso_id)
                ce_update.update(**campos_update)
                # CI_update.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = "Error de argumentos, " + str(ex)
            print('ERROR cajas egresos, anular: '+str(ex))
            return False

    def can_delete(self, nombre_campo, id_valor, **app_modelo):
        """verificando si se puede eliminar la tabla"""
        # verificamos si es operacion externa
        try:
            ce_check = CajasEgresos.objects.get(pk=id_valor)
            if ce_check.caja_movimiento_id > 0 or ce_check.venta_id > 0:
                self.error_operation = 'Debe anular esta operacion desde su origen'
                return False

            self.error_operation = ''
            return True

        except Exception as ex:
            self.error_operation = 'No se pudo verificar el registro, ' + str(ex)
            return False

    def permission_print(self, user_perfil, module, id):
        """permission to print caja ingreso"""
        caja_egreso = CajasEgresos.objects.get(pk=id)

        puede_imprimir = False
        if user_perfil.perfil_id.perfil_id == settings.PERFIL_ADMIN:
            puede_imprimir = True

        if user_perfil.perfil_id.perfil_id == settings.PERFIL_SUPERVISOR:
            punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)
            filtro_supervisor = {}
            filtro_supervisor['punto_id__sucursal_id'] = punto.sucursal_id
            filtro_supervisor['status_id'] = self.status_activo
            cajas_punto = apps.get_model('configuraciones', 'Cajas').objects.filter(**filtro_supervisor)
            for caja_punto in cajas_punto:
                if caja_egreso.caja_id == caja_punto:
                    puede_imprimir = True

        if user_perfil.perfil_id.perfil_id == settings.PERFIL_CAJERO:
            if caja_egreso.caja_id.caja_id == user_perfil.caja_id:
                puede_imprimir = True

        if not puede_imprimir:
            self.error_operation = "No tiene permiso para imprimir este recibo"

        return puede_imprimir
