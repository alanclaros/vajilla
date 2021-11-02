from utils.permissions import current_date
from django.conf import settings
from django.apps import apps
from django.db.models.query import QuerySet
from django.db.models import Sum

from controllers.DefaultValues import DefaultValues
# from status.models import Status
# from configuraciones.models import Cajas, Monedas, TiposMonedas, Puntos, Sucursales
# from cajas.models import CajasOperaciones, CajasOperacionesDetalles, CajasIngresos, CajasEgresos

# from utils.funciones_db import getMaxId
# from utils.fechas import get_date_to_db
from utils.dates_functions import get_date_to_db

# transaciones
from django.db import transaction


class CajasController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        # redifiniendo valores de ValoresDefecto
        self.modelo_name = 'CajasOperaciones'
        self.modelo_id = 'caja_operacion_id'  # id del usuario
        self.modelo_app = 'cajas'
        self.modulo_id = int(settings.MOD_INICIAR_CAJA)

        # control form
        self.control_form = ""
        self.modulo_session = "cajas_operaciones"

    def index_operations(self, user_perfil, user, operation):
        """
        cajas list according user_perfil
        :param user_perfil: (object) UserPerfil
        :param operation: (str) iniciar, iniciar_recibir, entregar, entregar_recibir
        :return: (list): cajas list
        """

        # cajas de la sucursal para usuario administrador y supervisor
        if user_perfil.perfil_id.perfil_id == self.perfil_admin or user_perfil.perfil_id.perfil_id == self.perfil_supervisor:
            if operation == 'iniciar' or operation == 'entregar_recibir':
                # todas las cajas de la sucursal
                user_punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)
                user_sucursal = apps.get_model('configuraciones', 'Sucursales').objects.get(pk=user_punto.sucursal_id.sucursal_id)

                # filtros
                self.filtros_modulo.clear()
                self.filtros_modulo['status_id'] = self.status_activo
                self.filtros_modulo['punto_id__sucursal_id'] = user_sucursal
                self.filtros_modulo['punto_id__status_id'] = self.status_activo

                cajas = apps.get_model('configuraciones', 'Cajas').objects.select_related('tipo_moneda_id').select_related('punto_id').filter(**self.filtros_modulo).order_by('punto_id__punto', 'caja')

            else:
                # solo cajas del punto
                user_punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)

                # filtros
                self.filtros_modulo.clear()
                self.filtros_modulo['status_id'] = self.status_activo
                self.filtros_modulo['punto_id'] = user_punto
                self.filtros_modulo['punto_id__status_id'] = self.status_activo

                cajas = apps.get_model('configuraciones', 'Cajas').objects.select_related('tipo_moneda_id').select_related('punto_id').filter(**self.filtros_modulo).order_by('caja')

        else:
            # solo cajas del cajero
            user_punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)
            user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=user)

            # filtros
            self.filtros_modulo.clear()
            self.filtros_modulo['status_id'] = self.status_activo
            self.filtros_modulo['punto_id'] = user_punto
            self.filtros_modulo['caja_id'] = user_perfil.caja_id
            self.filtros_modulo['punto_id__status_id'] = self.status_activo

            cajas = apps.get_model('configuraciones', 'Cajas').objects.select_related('tipo_moneda_id').select_related('punto_id').filter(**self.filtros_modulo).order_by('caja')

        return cajas

    def cash_status(self, fecha, Cajas, formato_ori='dd-MMM-yyyy'):
        """
        status for each cash for fecha as date
        :param fecha: (str) yyyy-mm-dd database format
        :param Cajas: (QuerySet) or (object) cash object(s)
        :param formato_ori: (str) date format
        :return: (list) cash and operation for day
        """
        retorno = {}
        fecha_query = get_date_to_db(fecha, formato_ori=formato_ori, formato='yyyy-mm-dd')

        if type(Cajas) == QuerySet or type(Cajas) == list:
            # cajas lista
            for caja in Cajas:
                # estado de caja para la fecha
                caja_fecha = apps.get_model('cajas', 'CajasOperaciones').objects.filter(caja_id=caja, fecha=fecha_query)
                if caja_fecha:
                    caja_day = caja_fecha.first()
                    # for key, value in cajaFecha.__dict__.items():
                    #     print('key:', key, ' value:', value)

                    retorno[caja.caja_id] = caja_day.status_id.status_id
                else:
                    retorno[caja.caja_id] = self.no_aperturado
        else:
            # caja object
            caja_fecha = apps.get_model('cajas', 'CajasOperaciones').objects.filter(caja_id=Cajas, fecha=fecha_query)
            if caja_fecha:
                caja_day = caja_fecha.first()
                retorno[Cajas.caja_id] = caja_day.status_id.status_id
            else:
                retorno[Cajas.caja_id] = self.no_aperturado

        return retorno

    def cash_active(self, fecha, user, formato_ori='dd-MMM-yyyy'):
        """
        get cajas actives for fecha as date according user
        :param fecha:(str) yyyy-mm-dd database format
        :param user: user request cajas (admin, supervisor, cajero)
        :param formato_ori: (str) date format
        :return: (list) cajas actives
        """

        # lista de cajas segun el perfil de usuario
        user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=user)
        user_punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)

        # en caso mostrar varias cajas
        # filtro = {}
        # filtro['status_id'] = self.status_activo
        # if user_perfil.perfil_id.perfil_id == self.perfil_admin or user_perfil.perfil_id.perfil_id == self.perfil_supervisor:
        #     # cajas activas de la sucursal
        #     filtro['punto_id__sucursal_id'] = user_punto.sucursal_id
        # else:
        #     # cajas activas para el punto
        #     filtro['punto_id'] = user_punto
        #
        # cajas_lista = apps.get_model('configuraciones', 'Cajas').objects.select_related('punto_id').select_related('tipo_moneda_id').filter(**filtro).order_by('punto_id__punto', 'caja')

        # solo mostramos la caja del usuario en caso de ingresos o egresos
        filtro = {}
        filtro['status_id'] = self.status_activo
        filtro['caja_id'] = user_perfil.caja_id
        cajas_lista = apps.get_model('configuraciones', 'Cajas').objects.select_related('punto_id').select_related('tipo_moneda_id').filter(**filtro).order_by('punto_id__punto', 'caja')

        estado_cajas = self.cash_status(fecha, cajas_lista, formato_ori=formato_ori)

        retorno = []

        for caja in cajas_lista:
            if estado_cajas[caja.caja_id] == self.apertura_recibe:
                retorno.append(caja)

        return retorno

    def day_balance(self, fecha, Cajas, formato_ori='dd-MMM-yyyy'):
        """fecha en formato yyyy-mm-dd, lista de cajas"""
        retorno = {}
        fecha_query = get_date_to_db(fecha, formato_ori=formato_ori, formato='yyyy-mm-dd')
        #print('fecha query: ', fecha_query)

        if type(Cajas) == QuerySet or type(Cajas) == list:
            # print('tipo', type(Cajas))
            for caja in Cajas:
                # estado de caja para la fecha
                caja_fecha = apps.get_model('cajas', 'CajasOperaciones').objects.filter(caja_id=caja, fecha=fecha_query)
                if caja_fecha:
                    caja_dia = caja_fecha.first()
                    saldo = caja_dia.monto_apertura

                    # ingresos y egresos
                    filtro = {}
                    filtro['caja_id'] = caja
                    filtro['status_id'] = self.status_activo
                    filtro['fecha__gte'] = get_date_to_db(fecha=fecha, formato_ori=formato_ori, formato='yyyy-mm-dd HH:ii:ss', tiempo='00:00:00')
                    filtro['fecha__lte'] = get_date_to_db(fecha=fecha, formato_ori=formato_ori, formato='yyyy-mm-dd HH:ii:ss', tiempo='23:59:59')
                    # print(filtro)

                    query = apps.get_model('cajas', 'CajasIngresos').objects.filter(**filtro).aggregate(Sum('monto'))
                    suma_ingresos = 0
                    if query['monto__sum']:
                        suma_ingresos = query['monto__sum']

                    # suma_ingresos = query.first()
                    # for k, v in suma_ingresos.__dict__.items():
                    #    print('k:', k, ' v:', v)

                    query = apps.get_model('cajas', 'CajasEgreos').objects.filter(**filtro).aggregate(Sum('monto'))
                    suma_egresos = 0
                    if query['monto__sum']:
                        suma_egresos = query['monto__sum']

                    saldo = saldo + suma_ingresos - suma_egresos

                    retorno[caja.caja_id] = saldo

                else:
                    retorno[caja.caja_id] = '/N'
        else:
            # caja object
            caja_fecha = apps.get_model('cajas', 'CajasOperaciones').objects.filter(caja_id=Cajas, fecha=fecha_query)
            #print('caja fecha: ', caja_fecha)
            if caja_fecha:
                caja_dia = caja_fecha.first()
                saldo = caja_dia.monto_apertura

                # ingresos y egresos
                filtro = {}
                filtro['caja_id'] = Cajas
                filtro['status_id'] = self.status_activo
                filtro['fecha__gte'] = get_date_to_db(fecha=fecha, formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss', tiempo='00:00:00')
                filtro['fecha__lte'] = get_date_to_db(fecha=fecha, formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss', tiempo='23:59:59')

                # ingresos
                query = apps.get_model('cajas', 'CajasIngresos').objects.filter(**filtro).aggregate(Sum('monto'))
                suma_ingresos = 0
                if query['monto__sum']:
                    suma_ingresos = query['monto__sum']

                # egresos
                query = apps.get_model('cajas', 'CajasEgresos').objects.filter(**filtro).aggregate(Sum('monto'))
                suma_egresos = 0
                if query['monto__sum']:
                    suma_egresos = query['monto__sum']

                saldo = saldo + suma_ingresos - suma_egresos

                retorno[Cajas.caja_id] = saldo

            else:
                retorno[Cajas.caja_id] = '/N'

        return retorno

    def add_operation(self, operation, fecha, Caja, formato_ori='dd-MMM-yyyy'):
        """
        verify if user can make operation with this cash
        :param operation: (str) operation to do
        :param fecha: (object) date for operation
        :param Caja: (object) cash object
        :param formato_ori: (str) in case date is str, original format
        :return: True if can make operation else False
        """

        estado_caja = self.cash_status(fecha, Caja, formato_ori=formato_ori)
        # print('estado_caja', estado_caja)

        if operation == 'iniciar':
            # verificamos que no tenga ningun estado
            if estado_caja[Caja.caja_id] == self.no_aperturado:
                return True

        if operation == 'iniciar_cancelar':
            # verificamos que este en estado iniciar
            if estado_caja[Caja.caja_id] == self.apertura:
                return True

        if operation == 'iniciar_recibir':
            # verificamos que este en estado apertura
            if estado_caja[Caja.caja_id] == self.apertura:
                return True

        if operation == 'iniciar_recibir_cancelar':
            # verificamos que este en estado apertura-recibe
            if estado_caja[Caja.caja_id] == self.apertura_recibe:
                return True

        if operation == 'entregar':
            # verificamos que no tenga ningun estado
            if estado_caja[Caja.caja_id] == self.apertura_recibe:
                return True

        if operation == 'entregar_cancelar':
            # verificamos que este en estado correcto
            if estado_caja[Caja.caja_id] == self.cierre:
                return True

        if operation == 'entregar_recibir':
            # verificamos el estado
            if estado_caja[Caja.caja_id] == self.cierre:
                return True

        if operation == 'entregar_recibir_cancelar':
            # verificamos que este en estado correcto
            if estado_caja[Caja.caja_id] == self.cierre_recibe:
                return True

        return False

    def get_coins(self, fecha, Caja, formato_ori='dd-MMM-yyyy'):
        """
        get coins for this cash
        :param fecha: (object) dato
        :param Caja: (object) cash object
        :param formato_ori: (str) in case date is string
        :return: (list) list coins
        """
        estado_caja = self.cash_status(fecha, Caja, formato_ori=formato_ori)
        retorno = []
        fecha_query = get_date_to_db(fecha, formato_ori=formato_ori, formato='yyyy-mm-dd')

        tipo_moneda = apps.get_model('configuraciones', 'TiposMonedas').objects.get(pk=Caja.tipo_moneda_id.tipo_moneda_id)

        if estado_caja[Caja.caja_id] == self.no_aperturado:
            monedas = apps.get_model('configuraciones', 'Monedas').objects.filter(tipo_moneda_id=tipo_moneda, status_id=self.status_activo).select_related('tipo_moneda_id').order_by('moneda_id')

            # monedas = Monedas.objects.filter(tipo_moneda_id=tipo_bs, status_id=status_activo).prefetch_related('tipo_moneda_id').order_by('moneda_id')
            # for key, value in monedas.__dict__.items():
            #     print('key:', key, 'value:', value)

            for moneda in monedas:
                # print(moneda.monto, '-', moneda.tipo_moneda_id.tipo_moneda)
                # for key, value in moneda.__dict__.items():
                retorno.append({'moneda_id': moneda.moneda_id, 'monto': moneda.monto, 'cantidad_apertura': 0, 'cantidad_cierre': 0, 'codigo': tipo_moneda.codigo})

        # elif estado_caja[Caja.caja_id] == self.apertura:
        else:
            # tiene estado distinto de no aperturado
            caja_operacion = apps.get_model('cajas', 'CajasOperaciones').objects.get(caja_id=Caja, fecha=fecha_query)
            detalles = apps.get_model('cajas', 'CajasOperacionesDetalles').objects.filter(caja_operacion_id=caja_operacion).select_related('moneda_id').order_by('moneda_id')
            for detalle in detalles:
                retorno.append({'moneda_id': detalle.moneda_id, 'monto': detalle.moneda_id.monto, 'cantidad_apertura': detalle.cantidad_apertura, 'cantidad_cierre': detalle.cantidad_cierre, 'codigo': tipo_moneda.codigo})

        return retorno

    def save_data(self, fecha, Caja, operation, request, formato_ori='dd-MMM-yyyy'):
        #fecha_query = get_date_to_db(fecha, formato_ori=formato_ori, formato='yyyy-mm-dd')
        fecha_query = fecha  # yyyy-mm-dd
        usuario_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
        #print('fecha: ', fecha, ' tam: ', len(fecha))
        # print('fecha query: ', fecha_query, ' fecha: ', fecha, ' formato_ori: ', formato_ori)
        try:
            # transaccion base de datos
            with transaction.atomic():

                estado_caja = self.cash_status(fecha, Caja, formato_ori=formato_ori)
                tipo_moneda = apps.get_model('configuraciones', 'TiposMonedas').objects.get(pk=Caja.tipo_moneda_id.tipo_moneda_id)

                if operation == 'iniciar_guardar':
                    if estado_caja[Caja.caja_id] == self.no_aperturado:
                        # estado correcto
                        monto_total = 0
                        monedas = apps.get_model('configuraciones', 'Monedas').objects.filter(tipo_moneda_id=tipo_moneda, status_id=self.status_activo).select_related('tipo_moneda_id').order_by('moneda_id')
                        for moneda in monedas:
                            dato = request.POST['moneda_' + str(moneda.moneda_id)].strip()

                            cantidad = 0 if dato == '' else int(dato)
                            monto_total += cantidad * moneda.monto

                        # caja_operacion_id = getMaxId('cajas', 'CajasOperaciones', 'caja_operacion_id')
                        caja_operacion = apps.get_model('cajas', 'CajasOperaciones').objects.create(fecha=fecha_query, monto_apertura=monto_total, usuario_perfil_apertura_id=usuario_perfil.user_perfil_id,
                                                                                                    usuario_perfil_apertura_r_id=0, monto_cierre=0, usuario_perfil_cierre_id=0, usuario_perfil_cierre_r_id=0, created_at='now', updated_at='now', caja_id=Caja, status_id=self.status_apertura)
                        caja_operacion.save()

                        # detalles
                        for moneda in monedas:
                            # caja_operacion_detalle_id = getMaxId('cajas', 'CajasOperacionesDetalles', 'caja_operacion_detalle_id')

                            dato = request.POST['moneda_' + str(moneda.moneda_id)].strip()
                            cantidad_apertura = 0 if dato == '' else int(dato)

                            detalle = apps.get_model('cajas', 'CajasOperacionesDetalles').objects.create(caja_operacion_id=caja_operacion, moneda_id=moneda, cantidad_apertura=cantidad_apertura, cantidad_cierre=0)
                            detalle.save()

                        return True

                if operation == 'iniciar_cancelar':
                    if estado_caja[Caja.caja_id] == self.apertura:
                        # estado correcto
                        caja_operacion = apps.get_model('cajas', 'CajasOperaciones').objects.get(caja_id=Caja, fecha=fecha_query)
                        detalles = apps.get_model('cajas', 'CajasOperacionesDetalles').objects.filter(caja_operacion_id=caja_operacion)
                        # eliminamos
                        detalles.delete()
                        caja_operacion.delete()

                        return True

                if operation == 'iniciar_recibir_guardar':
                    if estado_caja[Caja.caja_id] == self.apertura:
                        # estado correcto
                        caja_operacion = apps.get_model('cajas', 'CajasOperaciones').objects.get(caja_id=Caja, fecha=fecha_query)
                        caja_operacion.usuario_perfil_apertura_r_id = usuario_perfil.user_perfil_id
                        caja_operacion.status_id = self.status_apertura_recibe
                        caja_operacion.updated_at = 'now'
                        caja_operacion.save()

                        return True

                if operation == 'iniciar_recibir_cancelar':
                    if estado_caja[Caja.caja_id] == self.apertura_recibe:
                        # estado correcto
                        operacion = apps.get_model('cajas', 'CajasOperaciones').objects.get(caja_id=Caja, fecha=fecha_query)
                        operacion.usuario_perfil_apertura_r_id = 0
                        operacion.status_id = self.status_apertura
                        operacion.updated_at = 'now'
                        operacion.save()

                        return True

                if operation == 'entregar_guardar':
                    if estado_caja[Caja.caja_id] == self.apertura_recibe:
                        # estado correcto
                        monto_total = 0
                        monedas = apps.get_model('configuraciones', 'Monedas').objects.filter(tipo_moneda_id=tipo_moneda, status_id=self.status_activo).select_related('tipo_moneda_id').order_by('moneda_id')
                        for moneda in monedas:
                            dato = request.POST['moneda_' + str(moneda.moneda_id)].strip()

                            cantidad = 0 if dato == '' else int(dato)
                            monto_total += cantidad * moneda.monto

                        operacion = apps.get_model('cajas', 'CajasOperaciones').objects.get(caja_id=Caja, fecha=fecha_query)
                        operacion.monto_cierre = monto_total
                        operacion.usuario_perfil_cierre_id = usuario_perfil.user_perfil_id
                        operacion.status_id = self.status_cierre
                        operacion.updated_at = 'now'
                        operacion.save()

                        # detalles
                        for moneda in monedas:
                            dato = request.POST['moneda_' + str(moneda.moneda_id)].strip()
                            cantidad_cierre = 0 if dato == '' else int(dato)

                            detalle = apps.get_model('cajas', 'CajasOperacionesDetalles').objects.get(caja_operacion_id=operacion, moneda_id=moneda)
                            detalle.cantidad_cierre = cantidad_cierre
                            detalle.save()

                        return True

                if operation == 'entregar_cancelar':
                    if estado_caja[Caja.caja_id] == self.cierre:
                        # estado correcto
                        operacion = apps.get_model('cajas', 'CajasOperaciones').objects.get(caja_id=Caja, fecha=fecha_query)
                        operacion.monto_cierre = 0
                        operacion.usuario_perfil_cierre_id = 0
                        operacion.status_id = self.status_apertura_recibe
                        operacion.updated_at = 'now'
                        operacion.save()

                        # detalle
                        monedas = apps.get_model('configuraciones', 'Monedas').objects.filter(tipo_moneda_id=tipo_moneda, status_id=self.status_activo).select_related('tipo_moneda_id').order_by('moneda_id')
                        for moneda in monedas:
                            detalle = apps.get_model('cajas', 'CajasOperacionesDetalles').objects.get(caja_operacion_id=operacion, moneda_id=moneda)
                            detalle.cantidad_cierre = 0
                            detalle.save()

                        return True

                if operation == 'entregar_recibir_guardar':
                    if estado_caja[Caja.caja_id] == self.cierre:
                        # estado correcto
                        caja_operacion = apps.get_model('cajas', 'CajasOperaciones').objects.get(caja_id=Caja, fecha=fecha_query)
                        caja_operacion.usuario_perfil_cierre_r_id = usuario_perfil.user_perfil_id
                        caja_operacion.status_id = self.status_cierre_recibe
                        caja_operacion.updated_at = 'now'
                        caja_operacion.save()

                        return True

                if operation == 'entregar_recibir_cancelar':
                    if estado_caja[Caja.caja_id] == self.cierre_recibe:
                        # estado correcto
                        operacion = apps.get_model('cajas', 'CajasOperaciones').objects.get(caja_id=Caja, fecha=fecha_query)
                        operacion.usuario_perfil_cierre_r_id = 0
                        operacion.status_id = self.status_cierre
                        operacion.updated_at = 'now'
                        operacion.save()

                        return True

                # retorna error por defecto si no entro a ninguna operacion permitida
                return False

        except Exception as e:
            print('ERROR, operacion caja: ' + str(e))
            self.error_operation = "Error al realizar la operacion"
            return False
