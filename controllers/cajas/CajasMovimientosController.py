from django.conf import settings
from django.apps import apps
from django.contrib.auth.models import User

from utils.permissions import current_date, get_system_settings
from utils.dates_functions import get_date_show, get_date_to_db, get_seconds_date1_sub_date2
from controllers.DefaultValues import DefaultValues

from configuraciones.models import Cajas
from cajas.models import CajasMovimientos, CajasIngresos, CajasEgresos
from status.models import Status
from decimal import Decimal

# clases
from controllers.cajas.CajasController import CajasController
from controllers.cajas.CajasIngresosController import CajasIngresosController
from controllers.cajas.CajasEgresosController import CajasEgresosController

from utils.validators import validate_string, validate_number_int, validate_number_decimal

# transacciones
from django.db import transaction


class CajasMovimientosController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'CajasMovimientos'
        self.modelo_id = 'caja_movimiento_id'
        self.modelo_app = 'cajas'
        self.modulo_id = settings.MOD_CAJAS_MOVIMIENTOS

        # filtros de envio y recepcion
        self.filtros_envio = {}
        self.filtros_recepcion = {}
        self.fecha_operacion = current_date()

        # variables de session
        self.modulo_session = "cajas_movimientos"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {}

        # control del formulario
        self.control_form = "txt|1|S|monto|Monto"
        self.control_form += ";txt|2|S|concepto|Concepto"
        self.control_form += ";cbo|0|S|caja2|Caja Destino"

    def index_envio(self, punto_operacion, request):
        #ValoresDefecto.index(self, request)

        self.filtros_envio.clear()
        # status
        self.filtros_envio['status_id_id__in'] = [self.movimiento_caja, self.movimiento_caja_recibe, self.anulado]
        # fecha
        self.filtros_envio['fecha__gte'] = get_date_to_db(fecha=self.fecha_operacion, formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss', tiempo='00:00:00')
        self.filtros_envio['fecha__lte'] = get_date_to_db(fecha=self.fecha_operacion, formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss', tiempo='23:59:59')

        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        usuario_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
        retorno = []

        if usuario_perfil.perfil_id.perfil_id == settings.PERFIL_ADMIN:
            # todas las sucursales
            retorno = modelo.objects.select_related('caja1_id').select_related('caja1_user_perfil_id').select_related('caja2_id').select_related(
                'caja2_user_perfil_id').select_related('tipo_moneda_id').filter(**self.filtros_envio).order_by('fecha')

        if usuario_perfil.perfil_id.perfil_id == settings.PERFIL_SUPERVISOR:
            # sucursal
            punto_usuario = apps.get_model('configuraciones', 'Puntos').objects.get(pk=usuario_perfil.punto_id)
            self.filtros_envio['caja1_id__punto_id__sucursal_id'] = punto_usuario.sucursal_id
            retorno = modelo.objects.select_related('caja1_id').select_related('caja1_user_perfil_id').select_related('caja2_id').select_related(
                'caja2_user_perfil_id').select_related('tipo_moneda_id').filter(**self.filtros_envio).order_by('fecha')

        if usuario_perfil.perfil_id.perfil_id == settings.PERFIL_CAJERO:
            # sucursal
            self.filtros_envio['caja1_id__punto_id__punto_id'] = usuario_perfil.punto_id
            #print('filtros...:', self.filtros_envio)
            retorno = modelo.objects.select_related('caja1_id').select_related('caja1_user_perfil_id').select_related('caja2_id').select_related(
                'caja2_user_perfil_id').select_related('tipo_moneda_id').filter(**self.filtros_envio).order_by('fecha')

        # for sucursal in retorno:
        #    # print(ciudad.__dict__)
        #    print(sucursal.ciudad_id.pais_id.__dict__)

        return retorno

    def index_recepcion(self, punto_operacion, request):
        self.filtros_recepcion.clear()
        # status
        self.filtros_recepcion['status_id_id__in'] = [self.movimiento_caja, self.movimiento_caja_recibe, self.anulado]
        # caja
        #self.filtros_recepcion['caja2_id__punto_id'] = punto_operacion
        # fecha
        self.filtros_recepcion['fecha__gte'] = get_date_to_db(fecha=self.fecha_operacion, formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss', tiempo='00:00:00')
        self.filtros_recepcion['fecha__lte'] = get_date_to_db(fecha=self.fecha_operacion, formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss', tiempo='23:59:59')

        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        usuario_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
        retorno = []
        if usuario_perfil.perfil_id.perfil_id == settings.PERFIL_ADMIN:
            # todas las sucursales
            retorno = modelo.objects.select_related('caja1_id').select_related('caja1_user_perfil_id').select_related('caja2_id').select_related(
                'caja2_user_perfil_id').select_related('tipo_moneda_id').filter(**self.filtros_recepcion).order_by('fecha')

        if usuario_perfil.perfil_id.perfil_id == settings.PERFIL_SUPERVISOR:
            # sucursal
            punto_usuario = apps.get_model('configuraciones', 'Puntos').objects.get(pk=usuario_perfil.punto_id)
            self.filtros_recepcion['caja2_id__punto_id__sucursal_id'] = punto_usuario.sucursal_id
            retorno = modelo.objects.select_related('caja1_id').select_related('caja1_user_perfil_id').select_related('caja2_id').select_related(
                'caja2_user_perfil_id').select_related('tipo_moneda_id').filter(**self.filtros_recepcion).order_by('fecha')

        if usuario_perfil.perfil_id.perfil_id == settings.PERFIL_CAJERO:
            # sucursal
            self.filtros_recepcion['caja2_id__punto_id__punto_id'] = usuario_perfil.punto_id
            retorno = modelo.objects.select_related('caja1_id').select_related('caja1_user_perfil_id').select_related('caja2_id').select_related(
                'caja2_user_perfil_id').select_related('tipo_moneda_id').filter(**self.filtros_recepcion).order_by('fecha')

        # retorno = modelo.objects.select_related('caja1_id').select_related('caja1_user_perfil_id').select_related('caja2_id').select_related(
        #     'caja2_user_perfil_id').select_related('tipo_moneda_id').filter(**self.filtros_recepcion).order_by('fecha')

        return retorno

    def add(self, fecha, request):
        """aniadimos una nuevo registro"""
        try:
            # verificamos las cajas
            aux_c1 = validate_number_int('caja1', request.POST['caja1'])
            aux_c2 = validate_number_int('caja2', request.POST['caja2'])
            monto = validate_number_decimal('monto', request.POST['monto'])
            concepto = validate_string('concepto', request.POST['concepto'], remove_specials='yes')

            # caja, punto y usuario
            caja1 = Cajas.objects.get(pk=aux_c1)
            caja2 = Cajas.objects.get(pk=aux_c2)

            if caja1.tipo_moneda_id.tipo_moneda_id != caja2.tipo_moneda_id.tipo_moneda_id:
                self.error_operation = 'Ambas cajas deben tener la misma moneda'
                return False

            # saldo de caja
            caja_controller = CajasController()
            caja_saldo = caja_controller.day_balance(fecha, caja1, formato_ori='yyyy-mm-dd')

            saldo = caja_saldo[caja1.caja_id]
            if monto > saldo:
                self.error_operation = 'El monto no puede ser mayor al saldo de caja: ' + str(saldo)
                return False

            # suario
            usuario = request.user
            usuario_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=usuario)
            # estado
            status_cm = self.status_movimiento_caja

            # datos
            datos = {}
            datos['caja1_id'] = caja1
            datos['caja1_user_perfil_id'] = usuario_perfil
            datos['caja2_id'] = caja2
            datos['caja2_user_perfil_id'] = usuario_perfil
            datos['tipo_moneda_id'] = caja1.tipo_moneda_id
            datos['status_id'] = status_cm
            datos['fecha'] = fecha
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
            self.error_operation = "Error al agregar el movimiento de caja, " + str(ex)
            return False

    def add_db(self, **datos):
        """aniadimos a la base de datos"""
        try:
            with transaction.atomic():
                # caja, punto y usuario
                caja1 = datos['caja1_id']
                caja2 = datos['caja2_id']

                if caja1.tipo_moneda_id.tipo_moneda_id != caja2.tipo_moneda_id.tipo_moneda_id:
                    self.error_operation = 'Ambas cajas deben tener la misma moneda'
                    return False

                # saldo de caja
                caja_controller = CajasController()
                caja_saldo = caja_controller.day_balance(datos['fecha'], caja1, formato_ori='yyyy-mm-dd')

                saldo = caja_saldo[caja1.caja_id]
                if datos['monto'] > saldo:
                    self.error_operation = 'El monto no puede ser mayor al saldo de caja: ' + str(saldo)
                    return False

                # print(datos)
                campos_add = {}
                # campos fijos
                campos_add['caja1_id'] = datos['caja1_id']
                campos_add['caja1_user_perfil_id'] = datos['caja1_user_perfil_id']
                campos_add['caja2_id'] = datos['caja2_id']
                campos_add['caja2_user_perfil_id'] = datos['caja2_user_perfil_id']
                campos_add['tipo_moneda_id'] = datos['tipo_moneda_id']
                campos_add['status_id'] = datos['status_id']
                campos_add['fecha'] = get_date_to_db(fecha=datos['fecha'], formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss')
                campos_add['concepto'] = datos['concepto']
                campos_add['monto'] = datos['monto']
                campos_add['created_at'] = datos['created_at']
                campos_add['updated_at'] = datos['updated_at']

                # registramos
                cm_add = CajasMovimientos.objects.create(**campos_add)
                cm_add.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = "Error de argumentos, " + str(ex)
            print('ERROR cajas movimientos add, ' + str(ex))
            return False

    def anular_envio(self, request, id):
        # anulamos
        try:
            status_anulado = self.status_anulado
            usuario_anula = request.user.id
            user_perfil_anula = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=usuario_anula)
            motivo_anula = validate_string('motivo anula', request.POST['motivo_anula'], remove_specials='yes')

            # campos
            campos_update = {}
            campos_update['status_id'] = status_anulado
            campos_update['deleted_at'] = 'now'
            campos_update['user_perfil_id_anula'] = user_perfil_anula
            campos_update['motivo_anula'] = motivo_anula

            if self.anular_envio_db(id, **campos_update):
                self.error_operation = ""
                return True
            else:
                return False

        except Exception as ex:
            self.error_operation = 'error al anular, ' + str(ex)
            return False

    def anular_envio_db(self, caja_movimiento_id, **datos):
        """anulamos de la base de datos"""
        try:
            with transaction.atomic():
                caja_movimiento = CajasMovimientos.objects.get(pk=caja_movimiento_id)
                puede_anular = False
                if datos['user_perfil_id_anula'].perfil_id.perfil_id == settings.PERFIL_ADMIN:
                    # print('admin...')
                    puede_anular = True

                if datos['user_perfil_id_anula'].perfil_id.perfil_id == settings.PERFIL_SUPERVISOR:
                    punto_supervisor = apps.get_model('configuraciones', 'Puntos').objects.get(pk=datos['user_perfil_id_anula'].punto_id)
                    #print('supervisor...', punto_supervisor.sucursal_id, ' ...: ', caja_movimiento.caja1_id.punto_id.sucursal_id)
                    if punto_supervisor.sucursal_id == caja_movimiento.caja1_id.punto_id.sucursal_id:
                        puede_anular = True

                if datos['user_perfil_id_anula'].perfil_id.perfil_id == settings.PERFIL_CAJERO:

                    punto_cajero = apps.get_model('configuraciones', 'Puntos').objects.get(pk=datos['user_perfil_id_anula'].punto_id)
                    #print('cajero...', punto_cajero.punto_id, ' ...: ', caja_movimiento.caja1_id.punto_id.punto_id)
                    if punto_cajero.punto_id == caja_movimiento.caja1_id.punto_id.punto_id:
                        puede_anular = True

                if not puede_anular:
                    self.error_operation = "No tiene permiso para anular esta operacion"
                    return False

                # return False

                campos_update = {}
                # campos fijos
                campos_update['user_perfil_id_anula'] = datos['user_perfil_id_anula'].user_perfil_id
                campos_update['status_id'] = datos['status_id']
                campos_update['motivo_anula'] = datos['motivo_anula']
                campos_update['deleted_at'] = datos['deleted_at']

                # registramos
                cm_update = CajasMovimientos.objects.filter(pk=caja_movimiento_id)
                cm_update.update(**campos_update)

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = "Error de argumentos, " + str(ex)
            print('ERROR sucursales movimientos anular envio, ' + str(ex))
            return False

    def aceptar_recepcion(self, request, id):
        """recepciona el movimiento de caja"""
        try:
            status_recepcion = self.status_movimiento_caja_recibe
            usuario_recibe = request.user.id
            usuario_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=usuario_recibe)

            # campos
            campos_update = {}
            campos_update['status_id'] = status_recepcion
            campos_update['updated_at'] = get_date_to_db(fecha=current_date(), formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss')
            campos_update['caja2_user_perfil_id'] = usuario_perfil

            if self.aceptar_recepcion_db(id, **campos_update):
                self.error_operation = ""
                return True
            else:
                return False

        except Exception as ex:
            self.error_operation = 'error al recibir movimiento, ' + str(ex)
            return False

    def aceptar_recepcion_db(self, caja_movimiento_id, **datos):
        """recepciona el movimiento de caja, registro en la base de datos"""
        try:
            with transaction.atomic():
                # solo puede recibir el usuario de la caja
                caja_movimiento = CajasMovimientos.objects.select_for_update().get(pk=caja_movimiento_id)
                if not caja_movimiento.caja2_id.caja_id == datos['caja2_user_perfil_id'].caja_id:
                    self.error_operation = 'Un usuario de la caja ' + caja_movimiento.caja2_id.caja + ' debe recibir el monto'
                    return False

                # campos_update = {}
                # campos_update['status_id'] = datos['status_id']
                # campos_update['caja2_user_perfil_id'] = datos['caja2_user_perfil_id']
                # campos_update['updated_at'] = datos['updated_at']
                # # registramos
                # cm_update = CajasMovimientos.objects.filter(pk=caja_movimiento_id)
                # cm_update.update(**campos_update)
                sid_ini = transaction.savepoint()
                #print('sid ini...: ', sid_ini)

                caja_movimiento.status_id = datos['status_id']
                caja_movimiento.caja2_user_perfil_id = datos['caja2_user_perfil_id']
                caja_movimiento.updated_at = datos['updated_at']
                caja_movimiento.save()
                sid_cm = transaction.savepoint()
                #print('sid cm...: ', sid_cm)

                # registramos ingreso y egreso de caja
                ci_controller = CajasIngresosController()
                ce_controller = CajasEgresosController()
                status_activo = self.status_activo

                # ingreso
                #cm_update = CajasMovimientos.objects.get(pk=caja_movimiento_id)
                cm_update = caja_movimiento
                c_ingresos = {}
                c_ingresos['caja_movimiento_id'] = cm_update.caja_movimiento_id
                c_ingresos['fecha'] = datos['updated_at']
                c_ingresos['concepto'] = 'ingreso movimiento, ' + cm_update.concepto
                c_ingresos['monto'] = cm_update.monto
                c_ingresos['created_at'] = datos['updated_at']
                c_ingresos['updated_at'] = datos['updated_at']
                c_ingresos['caja_id'] = cm_update.caja2_id
                c_ingresos['punto_id'] = cm_update.caja2_id.punto_id
                c_ingresos['status_id'] = status_activo
                c_ingresos['user_perfil_id'] = cm_update.caja2_user_perfil_id
                # print(c_ingresos)
                if not ci_controller.add_db(**c_ingresos):
                    transaction.savepoint_rollback(sid_cm)
                    transaction.savepoint_rollback(sid_ini)
                    self.error_operation = 'error al registrar el ingreso'
                    return False

                sid_ci = transaction.savepoint()
                #print('sid ci...: ', sid_ci)

                # egreso
                c_egresos = {}
                c_egresos['caja_movimiento_id'] = cm_update.caja_movimiento_id
                c_egresos['fecha'] = datos['updated_at']
                c_egresos['concepto'] = 'egreso movimiento, ' + cm_update.concepto
                c_egresos['monto'] = cm_update.monto
                c_egresos['created_at'] = datos['updated_at']
                c_egresos['updated_at'] = datos['updated_at']
                c_egresos['caja_id'] = cm_update.caja1_id
                c_egresos['punto_id'] = cm_update.caja1_id.punto_id
                c_egresos['status_id'] = status_activo
                c_egresos['user_perfil_id'] = cm_update.caja1_user_perfil_id

                if not ce_controller.add_db(**c_egresos):
                    transaction.savepoint_rollback(sid_ci)
                    transaction.savepoint_rollback(sid_cm)
                    transaction.savepoint_rollback(sid_ini)
                    self.error_operation = 'error al registrar el egreso'
                    return False

                sid_ce = transaction.savepoint()
                #print('sid ce...: ', sid_ce)

                # commit transactions
                # print('antes ini')
                # if sid_ini:
                #     transaction.savepoint_commit(sid_ini)
                # print('antes cm: ', sid_cm)
                # if sid_cm:
                #     transaction.savepoint_commit(sid_cm)
                # print('antes ci')
                # if sid_ci:
                #     transaction.savepoint_commit(sid_ci)
                # print('antes ce')
                # if sid_ce:
                #     transaction.savepoint_commit(sid_ce)
                transaction.savepoint_commit(sid_ce)

                self.error_operation = ''
                return True

        except Exception as ex:
            print('exx: ', ex)
            self.error_operation = "Error de argumentos, " + str(ex)
            print('ERROR sucursales movimientos aceptar recepcion, ' + str(ex))
            return False

    def anular_recepcion(self, request, id):
        """anular, recepciona el movimiento de caja"""
        try:
            status_anula = self.status_anulado
            usuario_anula = request.user.id
            user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=usuario_anula)
            motivo_anula = validate_string('motivo anula', request.POST['motivo_anula'], remove_specials='yes')

            # campos
            campos_update = {}
            campos_update['status_id'] = status_anula
            campos_update['deleted_at'] = get_date_to_db(fecha=current_date(), formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss')
            campos_update['user_perfil_id_anula'] = user_perfil
            campos_update['motivo_anula'] = motivo_anula

            if self.anular_recepcion_db(id, **campos_update):
                self.error_operation = ""
                return True
            else:
                return False

        except Exception as ex:
            self.error_operation = 'error al anular, ' + str(ex)
            return False

    def anular_recepcion_db(self, caja_movimiento_id, **datos):
        """anula, recepciona el movimiento de caja, registro en la base de datos"""
        try:
            with transaction.atomic():
                caja_movimiento = CajasMovimientos.objects.get(pk=caja_movimiento_id)
                puede_anular = False
                if datos['user_perfil_id_anula'].perfil_id.perfil_id == settings.PERFIL_ADMIN:
                    # print('admin...')
                    puede_anular = True

                if datos['user_perfil_id_anula'].perfil_id.perfil_id == settings.PERFIL_SUPERVISOR:
                    punto_supervisor = apps.get_model('configuraciones', 'Puntos').objects.get(pk=datos['user_perfil_id_anula'].punto_id)
                    if punto_supervisor.sucursal_id == caja_movimiento.caja1_id.punto_id.sucursal_id:
                        puede_anular = True

                if datos['user_perfil_id_anula'].perfil_id.perfil_id == settings.PERFIL_CAJERO:
                    punto_cajero = apps.get_model('configuraciones', 'Puntos').objects.get(pk=datos['user_perfil_id_anula'].punto_id)
                    if punto_cajero.punto_id == caja_movimiento.caja1_id.punto_id.punto_id:
                        puede_anular = True

                if not puede_anular:
                    self.error_operation = "No tiene permiso para anular esta operacion"
                    return False

                # campos_update = {}
                # # campos fijos
                # campos_update['status_id'] = datos['status_id']
                # campos_update['user_perfil_id_anula'] = datos['user_perfil_id_anula'].user_perfil_id
                # campos_update['deleted_at'] = datos['deleted_at']
                # campos_update['motivo_anula'] = datos['motivo_anula']
                # # registramos
                # cm_update = CajasMovimientos.objects.filter(pk=caja_movimiento_id)
                # cm_update.update(**campos_update)
                sid_ini = transaction.savepoint()

                caja_movimiento.status_id = datos['status_id']
                caja_movimiento.user_perfil_id_anula = datos['user_perfil_id_anula'].user_perfil_id
                caja_movimiento.deleted_at = datos['deleted_at']
                caja_movimiento.motivo_anula = datos['motivo_anula']
                caja_movimiento.save()
                sid_cm = transaction.savepoint()

                # registramos ingreso y egreso de caja
                ci_controller = CajasIngresosController()
                ce_controller = CajasEgresosController()
                status_anulado = self.status_anulado

                cm_update = CajasMovimientos.objects.get(pk=caja_movimiento_id)
                filtro = {}
                filtro['caja_movimiento_id'] = cm_update.caja_movimiento_id
                filtro['caja_id'] = cm_update.caja2_id
                filtro['status_id'] = self.status_activo
                query = CajasIngresos.objects.filter(**filtro)
                #print('query ingreso: ', query)
                ci_up = query.first()

                # anulacion ingreso
                c_ingresos = {}
                c_ingresos['user_perfil_id_anula'] = datos['user_perfil_id_anula']
                c_ingresos['deleted_at'] = datos['deleted_at']
                c_ingresos['motivo_anula'] = datos['motivo_anula']
                c_ingresos['status_id'] = status_anulado
                #print('c ingresos: ', c_ingresos)
                if not ci_controller.delete_db(ci_up.caja_ingreso_id, **c_ingresos):
                    transaction.savepoint_rollback(sid_cm)
                    transaction.savepoint_rollback(sid_ini)
                    self.error_operation = 'error al anular el ingreso'
                    return False

                sid_ci = transaction.savepoint()

                # anulamos egreso
                filtro = {}
                filtro['caja_movimiento_id'] = cm_update.caja_movimiento_id
                filtro['caja_id'] = cm_update.caja1_id
                filtro['status_id'] = self.status_activo
                query = CajasEgresos.objects.filter(**filtro)
                ce_up = query.first()

                c_egresos = {}
                c_egresos['user_perfil_id_anula'] = datos['user_perfil_id_anula']
                c_egresos['deleted_at'] = datos['deleted_at']
                c_egresos['motivo_anula'] = datos['motivo_anula']
                c_egresos['status_id'] = status_anulado

                if not ce_controller.delete_db(ce_up.caja_egreso_id, **c_egresos):
                    transaction.savepoint_rollback(sid_ci)
                    transaction.savepoint_rollback(sid_cm)
                    transaction.savepoint_rollback(sid_ini)
                    self.error_operation = 'error al anular el egreso'
                    return False

                sid_ce = transaction.savepoint()

                # commit
                transaction.savepoint_commit(sid_ce)

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = "Error de argumentos, " + str(ex)
            print('ERROR sucursales movimientos anular recepcion, '+str(ex))
            return False
