from decimal import Decimal
from re import match
from typing import Match

from clientes.models import Clientes
from configuraciones.models import Almacenes, Puntos
from controllers.cajas.CajasEgresosController import CajasEgresosController
from controllers.cajas.CajasIngresosController import CajasIngresosController
from controllers.clientes.ClientesController import ClientesController
from controllers.DefaultValues import DefaultValues
from controllers.inventarios.StockController import StockController
from controllers.cajas.CajasController import CajasController
from django.apps import apps
from django.conf import settings
from django.db import connection, transaction
from inventarios.models import Stock
from permisos.models import UsersPerfiles
from productos.models import Productos
# fechas
from utils.dates_functions import (add_days_datetime, add_minutes_datetime,
                                   get_date_show, get_date_system,
                                   get_date_to_db, get_fecha_int,
                                   get_seconds_date1_sub_date2)
from utils.permissions import get_permissions_user, get_system_settings, current_date
from utils.validators import (validate_number_decimal, validate_number_int,
                              validate_string)

from ventas.models import (Ventas, VentasAumentos, VentasAumentosDetalles,
                           VentasDetalles)


class VentasController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Ventas'
        self.modelo_id = 'venta_id'
        self.modelo_app = 'ventas'
        self.modulo_id = settings.MOD_VENTAS

        # variables de session
        self.modulo_session = "ventas"
        self.columnas.append('fecha_evento')
        self.columnas.append('apellidos')
        self.columnas.append('nombres')

        self.variables_filtros.append('search_fecha_ini')
        self.variables_filtros.append('search_fecha_fin')
        self.variables_filtros.append('search_numero_contrato')
        self.variables_filtros.append('search_apellidos')
        self.variables_filtros.append('search_nombres')
        self.variables_filtros.append('search_ci_nit')

        fecha_actual = get_date_system()
        fecha_fin = get_date_show(fecha=fecha_actual, formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')
        fecha_ini = add_days_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd', dias=-7, formato='dd-MMM-yyyy')

        self.variables_filtros_defecto['search_fecha_ini'] = fecha_ini
        self.variables_filtros_defecto['search_fecha_fin'] = fecha_fin
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
        self.control_form = "txt|2|S|apellidos|Apellidos;"
        self.control_form += "txt|2|S|nombres|Nombres;"
        self.control_form += "txt|1|S|ci_nit|CI/NIT;"
        self.control_form += "txt|5|S|telefonos|Telefonos;"
        self.control_form += "txt|1|S|numero_contrato|Numero Contrato;"
        self.control_form += "txt|2|S|direccion_evento|Direccion Evento;"
        self.control_form += "txt|1|S|total_final|Total;"
        self.control_form += "txt|1|S|garantia_bs|Garantia"

    def index(self, request):
        DefaultValues.index(self, request)

        # ultimo acceso
        if 'last_access' in request.session[self.modulo_session].keys():
            # restamos
            resta = abs(get_seconds_date1_sub_date2(fecha1=get_date_system(time='yes'), formato1='yyyy-mm-dd HH:ii:ss', fecha2=request.session[self.modulo_session]['last_access'], formato2='yyyy-mm-dd HH:ii:ss'))
            # print('resta:', resta)
            if resta > 14400:  # 4 horas (4x60x60)
                # print('modificando')
                fecha_actual = get_date_system()
                fecha_inicio = add_days_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd', dias=-7, formato='dd-MMM-yyyy')
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
            request.session[self.modulo_session]['last_access'] = get_date_system(time='yes')
            request.session.modified = True
        else:
            request.session[self.modulo_session]['last_access'] = get_date_system(time='yes')
            request.session.modified = True

        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.anulado, self.preventa, self.venta, self.salida_almacen, self.vuelta_almacen, self.finalizado]

        # numero_contrato
        if self.variables_filtros_values['search_numero_contrato'].strip() != "":
            self.filtros_modulo['numero_contrato'] = self.variables_filtros_values['search_numero_contrato'].strip()
        else:
            # fechas
            if self.variables_filtros_values['search_fecha_ini'].strip() != '' and self.variables_filtros_values['search_fecha_fin'].strip() != '':
                self.filtros_modulo['fecha_evento__gte'] = get_date_to_db(fecha=self.variables_filtros_values['search_fecha_ini'].strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo='00:00:00')
                self.filtros_modulo['fecha_evento__lte'] = get_date_to_db(fecha=self.variables_filtros_values['search_fecha_fin'].strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo='23:59:59')

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
                if operation == self.salida_almacen or operation == self.vuelta_almacen:
                    return True

            if user_perfil.perfil_id.perfil_id == settings.PERFIL_CAJERO:
                if operation == self.preventa or operation == self.venta or operation == self.finalizado:
                    return True

            return False

        except Exception as ex:
            print('Error in permission operation, ', str(ex))
            return False

    def save(self, request, type='add'):
        """aniadimos un nuevo registro"""
        try:
            # punto
            usuario = request.user
            usuario_perfil = UsersPerfiles.objects.get(user_id=usuario)
            punto = Puntos.objects.get(pk=usuario_perfil.punto_id)
            #print('operation...: ', request.POST['operation'])
            if type == 'aumento_pedido':
                operation = validate_string('operation', request.POST['operation'])
            else:
                operation = validate_number_int('operation', request.POST['operation'], len_zero='yes')

            if not self.permission_operation(usuario_perfil, operation):
                self.error_operation = 'no tiene permiso para esta operacion'
                return False

            if operation == self.preventa:
                status_venta = self.status_preventa
                #almacen_id = validate_number_int('almacen', request.POST['almacen_id'])
                almacen_id = 1
                cliente_id = validate_number_int('cliente_id', request.POST['cliente_id'], len_zero='yes')
                id = validate_number_int('id', request.POST['id'], len_zero='yes')

                apellidos = validate_string('apellidos', request.POST['apellidos'], remove_specials='yes')
                nombres = validate_string('nombres', request.POST['nombres'], remove_specials='yes')
                ci_nit = validate_string('ci/nit', request.POST['ci_nit'], remove_specials='yes')
                telefonos = validate_string('telefonos', request.POST['telefonos'], remove_specials='yes')
                numero_contrato = validate_string('numero contrato', request.POST['numero_contrato'], remove_specials='yes')
                direccion_evento = validate_string('direccion evento', request.POST['direccion_evento'], remove_specials='yes')
                garantia_bs = validate_number_decimal('garantia', request.POST['garantia_bs'], len_zero='yes')

                factura_a = validate_string('factura_a', request.POST['factura_a'], remove_specials='yes', len_zero='yes')
                observacion = validate_string('observacion', request.POST['observacion'], remove_specials='yes', len_zero='yes')

                subtotal = validate_number_decimal('subtotal', request.POST['total_pedido'])
                descuento = validate_number_decimal('descuento', request.POST['descuento'], len_zero='yes')
                porcentaje_descuento = validate_number_decimal('porcentaje descuento', request.POST['porcentaje_descuento'], len_zero='yes')
                total = validate_number_decimal('total', request.POST['total_venta'])
                costo_transporte = validate_number_decimal('costo transporte', request.POST['costo_transporte'], len_zero='yes')
                total_final = validate_number_decimal('total final', request.POST['total_final'])

                aux = validate_string('fecha evento', request.POST['fecha_evento'], remove_specials='yes')
                fecha_evento = get_date_to_db(fecha=aux, formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd')

                aux = validate_string('fecha entrega', request.POST['fecha_entrega'], remove_specials='yes')
                fecha_entrega = get_date_to_db(fecha=aux, formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd')
                hora_entrega = validate_string('hora entrega', request.POST['hora_entrega'], remove_specials='yes')
                minuto_entrega = validate_string('minuto entrega', request.POST['minuto_entrega'], remove_specials='yes')

                aux = validate_string('fecha devolucion', request.POST['fecha_devolucion'], remove_specials='yes')
                fecha_devolucion = get_date_to_db(fecha=aux, formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd')
                hora_devolucion = validate_string('hora devolucion', request.POST['hora_devolucion'], remove_specials='yes')
                minuto_devolucion = validate_string('minuto devolucion', request.POST['minuto_devolucion'], remove_specials='yes')

                if almacen_id == 0:
                    self.error_operation = 'Debe Seleccionar el Almacen'
                    return False

                almacen = Almacenes.objects.get(pk=almacen_id)
                datos = {}
                datos['type'] = type
                datos['id'] = id
                datos['almacen_id'] = almacen
                datos['punto_id'] = punto
                datos['user_perfil_id'] = usuario_perfil

                datos['status_id'] = status_venta
                datos['operation'] = operation

                datos['fecha_evento'] = fecha_evento
                datos['fecha_entrega'] = fecha_entrega + ' ' + hora_entrega + ':' + minuto_entrega + ':00'
                datos['fecha_devolucion'] = fecha_devolucion + ' ' + hora_devolucion + ':' + minuto_devolucion + ':00'
                datos['cliente_id'] = cliente_id
                datos['apellidos'] = apellidos
                datos['nombres'] = nombres
                datos['numero_contrato'] = numero_contrato
                datos['direccion_evento'] = direccion_evento
                datos['garantia_bs'] = garantia_bs
                datos['ci_nit'] = ci_nit
                datos['telefonos'] = telefonos

                datos['factura_a'] = factura_a
                datos['observacion'] = observacion

                datos['subtotal'] = subtotal
                datos['descuento'] = descuento
                datos['porcentaje_descuento'] = porcentaje_descuento
                datos['costo_transporte'] = costo_transporte
                datos['total'] = total

                datos['created_at'] = 'now'
                datos['updated_at'] = 'now'

                # detalles del registro
                detalles = []
                for i in range(1, 51):
                    aux = request.POST['producto_' + str(i)].strip()
                    aux_5 = request.POST['cantidad_' + str(i)].strip()
                    aux_6 = request.POST['costo_' + str(i)].strip()
                    aux_7 = request.POST['detalle_' + str(i)].strip()

                    #print(aux, aux_2, aux_3)
                    if aux != '0' and aux_5 != '' and aux_6 != '':
                        dato_detalle = {}
                        dato_detalle['producto_id'] = Productos.objects.get(pk=int(aux))
                        dato_detalle['cantidad_salida'] = Decimal(aux_5)
                        dato_detalle['costo_salida'] = Decimal(aux_6)
                        dato_detalle['total_salida'] = dato_detalle['cantidad_salida'] * dato_detalle['costo_salida']
                        dato_detalle['detalle'] = aux_7

                        detalles.append(dato_detalle)

                #print('detalles: ', detalles)
                datos['detalles'] = detalles
                # verificando que haya detalles
                if len(detalles) == 0:
                    self.error_operation = 'debe registrar al menos un producto'
                    return False

                if self.save_preventa(**datos):
                    self.error_operation = ""
                    return True
                else:
                    return False

            if operation == self.venta:
                id = validate_number_int('id', request.POST['id'], len_zero='yes')
                almacen_id = 1
                almacen = Almacenes.objects.get(pk=almacen_id)
                datos = {}
                datos['operation'] = operation
                datos['id'] = id
                datos['almacen_id'] = almacen
                datos['user_perfil_id'] = usuario_perfil
                datos['updated_at'] = 'now'

                if self.save_venta(**datos):
                    self.error_operation = ""
                    return True
                else:
                    return False

            if operation == 'aumento_pedido':
                id = validate_number_int('id', request.POST['id'], len_zero='yes')
                subtotal = validate_number_decimal('subtotal', request.POST['total_pedido'])
                descuento = validate_number_decimal('descuento', request.POST['descuento'], len_zero='yes')
                porcentaje_descuento = validate_number_decimal('porcentaje descuento', request.POST['porcentaje_descuento'], len_zero='yes')
                total = validate_number_decimal('total', request.POST['total_venta'])
                costo_transporte = validate_number_decimal('costo transporte', request.POST['costo_transporte'], len_zero='yes')
                total_final = validate_number_decimal('total final', request.POST['total_final'])
                garantia_bs = validate_number_decimal('garantia', request.POST['garantia_bs'])
                observacion = validate_string('observacion', request.POST['observacion'], remove_specials='yes', len_zero='yes')

                almacen_id = 1
                almacen = Almacenes.objects.get(pk=almacen_id)
                datos = {}
                datos['operation'] = type
                datos['id'] = id
                datos['almacen_id'] = almacen
                datos['punto_id'] = punto
                datos['user_perfil_id'] = usuario_perfil
                datos['subtotal'] = subtotal
                datos['descuento'] = descuento
                datos['porcentaje_descuento'] = porcentaje_descuento
                datos['costo_transporte'] = costo_transporte
                datos['total'] = total
                datos['garantia_bs'] = garantia_bs
                datos['observacion'] = observacion
                datos['created_at'] = 'now'
                datos['updated_at'] = 'now'

                # detalles del registro
                detalles = []
                for i in range(1, 51):
                    aux = request.POST['producto_' + str(i)].strip()
                    aux_5 = request.POST['cantidad_' + str(i)].strip()
                    aux_6 = request.POST['costo_' + str(i)].strip()
                    aux_7 = request.POST['detalle_' + str(i)].strip()

                    #print(aux, aux_2, aux_3)
                    if aux != '0' and aux_5 != '' and aux_6 != '':
                        dato_detalle = {}
                        dato_detalle['producto_id'] = Productos.objects.get(pk=int(aux))
                        dato_detalle['cantidad_salida'] = Decimal(aux_5)
                        dato_detalle['costo_salida'] = Decimal(aux_6)
                        dato_detalle['total_salida'] = dato_detalle['cantidad_salida'] * dato_detalle['costo_salida']
                        dato_detalle['detalle'] = aux_7

                        detalles.append(dato_detalle)

                #print('detalles: ', detalles)
                datos['detalles'] = detalles
                # verificando que haya detalles
                if len(detalles) == 0:
                    self.error_operation = 'debe registrar al menos un producto'
                    return False

                if self.save_aumento(**datos):
                    self.error_operation = ""
                    return True
                else:
                    return False

            if operation == self.salida_almacen:
                id = validate_number_int('id', request.POST['id'], len_zero='yes')
                almacen_id = 1
                almacen = Almacenes.objects.get(pk=almacen_id)
                datos = {}
                datos['operation'] = operation
                datos['id'] = id
                datos['almacen_id'] = almacen
                datos['user_perfil_id'] = usuario_perfil
                datos['updated_at'] = 'now'

                if self.save_salida(**datos):
                    self.error_operation = ""
                    return True
                else:
                    return False

            if operation == self.vuelta_almacen:
                id = validate_number_int('id', request.POST['id'], len_zero='yes')
                almacen_id = 1
                almacen = Almacenes.objects.get(pk=almacen_id)
                datos = {}
                datos['operation'] = operation
                datos['id'] = id
                datos['almacen_id'] = almacen
                datos['user_perfil_id'] = usuario_perfil
                datos['updated_at'] = 'now'

                venta = Ventas.objects.get(pk=id)
                venta_detalles = VentasDetalles.objects.filter(venta_id=venta)

                # detalles del registro
                detalles = []
                i = 1
                for detalle in venta_detalles:
                    aux = request.POST['vuelta_' + str(i)].strip()
                    aux2 = request.POST['salida_' + str(i)].strip()
                    aux_5 = request.POST['rotura_' + str(i)].strip()
                    aux_6 = request.POST['refaccion_' + str(i)].strip()
                    if aux_6 == '':
                        refaccion = 0
                    else:
                        refaccion = Decimal(aux_6)

                    if aux != '' and aux2 != '' and aux_5 != '':
                        dato_detalle = {}
                        dato_detalle['producto_id'] = detalle.producto_id
                        dato_detalle['cantidad_salida'] = Decimal(aux2)
                        dato_detalle['cantidad_vuelta'] = Decimal(aux)
                        dato_detalle['rotura'] = Decimal(aux_5)
                        dato_detalle['refaccion'] = refaccion
                        dato_detalle['total_vuelta'] = 0

                        detalles.append(dato_detalle)

                    i += 1

                #print('detalles: ', detalles)
                datos['detalles'] = detalles
                # verificando que haya detalles
                if len(detalles) == 0:
                    self.error_operation = 'debe registrar al menos un producto'
                    return False

                if self.save_vuelta(**datos):
                    self.error_operation = ""
                    return True
                else:
                    return False

            if operation == self.finalizado:
                id = validate_number_int('id', request.POST['id'], len_zero='yes')
                almacen_id = 1
                almacen = Almacenes.objects.get(pk=almacen_id)
                datos = {}
                datos['operation'] = operation
                datos['id'] = id
                datos['almacen_id'] = almacen
                datos['user_perfil_id'] = usuario_perfil
                datos['updated_at'] = 'now'

                #print('datos para finalizar...: ', datos)
                if self.save_finalizado(**datos):
                    self.error_operation = ""
                    return True
                else:
                    return False

            self.error_operation = 'operation no valid'
            return False

        except Exception as ex:
            self.error_operation = "Error al agregar el registro, " + str(ex)
            return False

    def save_preventa(self, **datos):
        """aniadimos a la base de datos"""
        try:
            if len(datos['detalles']) == 0:
                self.error_operation = 'debe registrar al menos un producto'
                return False

            if not self.permission_operation(datos['user_perfil_id'], datos['operation']):
                self.error_operation = 'no puede realizar esta operacion'
                return False

            aux_f = get_date_to_db(fecha=datos['fecha_evento'], formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss', tiempo='00:00:00')
            #print('antes resta, ', datos['fecha_entrega'], ' , ', aux_f)
            resta = get_seconds_date1_sub_date2(fecha1=datos['fecha_entrega'], fecha2=aux_f)
            #print('resta..: ', resta)
            if resta < 0:
                self.error_operation = 'La fecha del evento es mayor a la fecha de entrega'

            resta = get_seconds_date1_sub_date2(fecha1=datos['fecha_devolucion'], fecha2=datos['fecha_entrega'])
            if resta < 0:
                self.error_operation = 'La fecha de entrega es mayor a la fecha de devolucion'
            dias_prestamo = int(resta/86400)  # 86400 segundos 1 dia

            stock_controller = StockController()
            cliente_controller = ClientesController()
            #print('antes transaccion')
            with transaction.atomic():
                campos_add = {}
                campos_add['almacen_id'] = datos['almacen_id']
                campos_add['punto_id'] = datos['punto_id']
                campos_add['user_perfil_id'] = datos['user_perfil_id']
                campos_add['status_id'] = datos['status_id']

                campos_add['fecha_evento'] = datos['fecha_evento']
                campos_add['fecha_entrega'] = datos['fecha_entrega']
                campos_add['fecha_devolucion'] = datos['fecha_devolucion']
                campos_add['dias'] = dias_prestamo

                if datos['cliente_id'] == 0:
                    # registramos nuevo cliente
                    datos_cliente = {}
                    if datos['ci_nit'] == '':
                        # no registramos, cliente sin nombre
                        datos['cliente_id'] = apps.get_model('clientes', 'Clientes').objects.get(pk=1)
                    else:
                        cliente_aux = apps.get_model('clientes', 'Clientes').objects.filter(ci_nit=datos['ci_nit'])
                        if cliente_aux:
                            primer_cliente = cliente_aux.first()
                            if primer_cliente.ci_nit == 0:
                                # no actualizamos el cliente por defecto 0
                                datos['cliente_id'] = apps.get_model('clientes', 'Clientes').objects.get(pk=1)
                            else:
                                # actualizamos datos
                                datos_cliente['apellidos'] = datos['apellidos']
                                datos_cliente['nombres'] = datos['nombres']
                                datos_cliente['ci_nit'] = datos['ci_nit']
                                datos_cliente['telefonos'] = datos['telefonos']
                                datos_cliente['direccion'] = datos['direccion_evento']
                                datos_cliente['email'] = primer_cliente.email
                                datos_cliente['razon_social'] = primer_cliente.razon_social
                                datos_cliente['factura_a'] = primer_cliente.factura_a
                                datos_cliente['updated_at'] = datos['updated_at']
                                datos_cliente['status_id'] = self.status_activo
                                datos_cliente['id'] = primer_cliente.cliente_id

                                if not cliente_controller.save_db(type='modify', **datos_cliente):
                                    self.error_operation = 'Error al actualizar datos del cliente'
                                    return False
                                datos['cliente_id'] = primer_cliente
                        else:
                            # creamos un nuevo cliente
                            datos_cliente['apellidos'] = datos['apellidos']
                            datos_cliente['nombres'] = datos['nombres']
                            datos_cliente['ci_nit'] = datos['ci_nit']
                            datos_cliente['telefonos'] = datos['telefonos']
                            datos_cliente['direccion'] = datos['direccion_evento']
                            datos_cliente['email'] = ''
                            datos_cliente['razon_social'] = datos['apellidos']
                            datos_cliente['factura_a'] = datos['apellidos']
                            datos_cliente['created_at'] = datos['created_at']
                            datos_cliente['updated_at'] = datos['updated_at']
                            datos_cliente['status_id'] = self.status_activo
                            datos_cliente['user_perfil_id'] = datos['user_perfil_id']
                            datos_cliente['punto_id'] = datos['punto_id']
                            datos_cliente['id'] = 0

                            if not cliente_controller.save_db(type='add', **datos_cliente):
                                self.error_operation = 'Error al crear el nuevo cliente'
                                return False

                            cliente_aux = apps.get_model('clientes', 'Clientes').objects.get(ci_nit=datos['ci_nit'])
                            datos['cliente_id'] = cliente_aux

                else:
                    # actualizamos datos
                    cliente_actual = apps.get_model('clientes', 'Clientes').objects.get(pk=datos['cliente_id'])
                    datos_cliente = {}
                    datos_cliente['apellidos'] = datos['apellidos']
                    datos_cliente['nombres'] = datos['nombres']
                    datos_cliente['ci_nit'] = datos['ci_nit']
                    datos_cliente['telefonos'] = datos['telefonos']
                    datos_cliente['direccion'] = datos['direccion_evento']
                    datos_cliente['email'] = cliente_actual.email
                    datos_cliente['razon_social'] = cliente_actual.razon_social
                    datos_cliente['factura_a'] = cliente_actual.factura_a
                    datos_cliente['updated_at'] = datos['updated_at']
                    datos_cliente['status_id'] = self.status_activo
                    datos_cliente['id'] = cliente_actual.cliente_id

                    if not cliente_controller.save_db(type='modify', **datos_cliente):
                        self.error_operation = 'Error al actualizar datos del cliente'
                        return False

                    datos['cliente_id'] = cliente_actual

                campos_add['cliente_id'] = datos['cliente_id']
                campos_add['apellidos'] = datos['apellidos']
                campos_add['nombres'] = datos['nombres']
                campos_add['numero_contrato'] = datos['numero_contrato']
                campos_add['direccion_evento'] = datos['direccion_evento']
                campos_add['garantia_bs'] = datos['garantia_bs']
                campos_add['ci_nit'] = datos['ci_nit']
                campos_add['telefonos'] = datos['telefonos']

                campos_add['factura_a'] = datos['factura_a']
                campos_add['observacion'] = datos['observacion']

                campos_add['subtotal'] = datos['subtotal']
                campos_add['descuento'] = datos['descuento']
                campos_add['porcentaje_descuento'] = datos['porcentaje_descuento']
                campos_add['costo_transporte'] = datos['costo_transporte']
                campos_add['total'] = 0
                campos_add['user_perfil_id_preventa'] = datos['user_perfil_id'].user_perfil_id
                campos_add['fecha_preventa'] = datos['updated_at']

                campos_add['updated_at'] = datos['updated_at']
                #print('campos add: ', campos_add)
                # venta
                if datos['type'] == 'add':
                    campos_add['created_at'] = datos['created_at']
                    venta_add = Ventas.objects.create(**campos_add)
                    venta_add.save()

                if datos['type'] == 'modify':
                    # eliminamos detalles
                    venta_actual = Ventas.objects.get(pk=datos['id'])
                    ventas_detalles_del = VentasDetalles.objects.filter(venta_id=venta_actual)
                    ventas_detalles_del.delete()

                    venta_actual = Ventas.objects.filter(pk=datos['id'])
                    venta_actual.update(**campos_add)
                    venta_add = Ventas.objects.get(pk=datos['id'])

                # detalles
                suma_subtotal = 0
                suma_descuento = 0
                suma_total = 0
                for detalle in datos['detalles']:
                    suma_subtotal += detalle['total_salida']
                    suma_total += detalle['total_salida']
                    detalle_add = VentasDetalles.objects.create(venta_id=venta_add, punto_id=datos['punto_id'], producto_id=detalle['producto_id'],
                                                                cantidad_salida=detalle['cantidad_salida'], costo_salida=detalle['costo_salida'], total_salida=detalle['total_salida'], detalle=detalle['detalle'])
                    detalle_add.save()

                    # actualizamos el stock
                    # stock_up = stock_controller.update_stock(user_perfil=datos['user_perfil_id'], almacen=datos['almacen_id'], producto=detalle['producto_id'], cantidad=0-detalle['cantidad_salida'])
                    # if not stock_up:
                    #     self.error_operation = 'Error al actualizar stock'
                    #     return False

                # actualizamos datos
                venta_add.subtotal = suma_subtotal
                venta_add.descuento = datos['descuento']
                venta_add.total = suma_total - datos['descuento'] + datos['costo_transporte']
                venta_add.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR registros add venta, '+str(ex))
            return False

    def save_venta(self, **datos):
        """aniadimos a la base de datos"""
        #print('datos..: ', datos)
        stock_controller = StockController()
        try:
            if not self.permission_operation(datos['user_perfil_id'], datos['operation']):
                self.error_operation = 'no puede realizar esta operacion'
                return False

            venta = Ventas.objects.get(pk=datos['id'])
            if venta.status_id != self.status_preventa:
                self.error_operation = 'esta operacion no es una preventa'
                return False

            # verificamos stock de productos
            venta_detalles = VentasDetalles.objects.filter(venta_id=venta)
            datos_productos = self.stock_productos(venta.fecha_entrega, venta.fecha_devolucion)
            for detalle in venta_detalles:
                p_id = detalle.producto_id.producto_id
                if datos_productos[p_id] < 0:
                    self.error_operation = 'No tiene stock suficiente'
                    return False

            with transaction.atomic():
                campos_add = {}
                campos_add['user_perfil_id_venta'] = datos['user_perfil_id'].user_perfil_id
                campos_add['fecha_venta'] = datos['updated_at']
                campos_add['updated_at'] = datos['updated_at']
                campos_add['status_id'] = self.status_venta

                venta_actual = Ventas.objects.filter(pk=datos['id'])
                venta_actual.update(**campos_add)

                for detalle in venta_detalles:
                    # actualizamos el stock
                    stock_up = stock_controller.update_stock(user_perfil=datos['user_perfil_id'], almacen=datos['almacen_id'], producto=detalle.producto_id, cantidad=0-detalle.cantidad_salida)
                    if not stock_up:
                        self.error_operation = 'Error al actualizar stock'
                        return False

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR registros add venta, '+str(ex))
            return False

    def save_aumento(self, **datos):
        """aniadimos a la base de datos"""
        stock_controller = StockController()
        try:
            if len(datos['detalles']) == 0:
                self.error_operation = 'debe registrar al menos un producto'
                return False

            if not self.permission_operation(datos['user_perfil_id'], datos['operation']):
                self.error_operation = 'no puede realizar esta operacion'
                return False

            venta = Ventas.objects.get(pk=datos['id'])
            with transaction.atomic():
                campos_add = {}
                campos_add['punto_id'] = datos['punto_id']
                campos_add['user_perfil_id'] = datos['user_perfil_id']
                campos_add['status_id'] = self.status_venta
                campos_add['venta_id'] = venta

                campos_add['subtotal'] = datos['subtotal']
                campos_add['descuento'] = datos['descuento']
                campos_add['porcentaje_descuento'] = datos['porcentaje_descuento']
                campos_add['costo_transporte'] = datos['costo_transporte']
                campos_add['garantia_bs'] = datos['garantia_bs']
                campos_add['observacion'] = datos['observacion']
                campos_add['total'] = 0

                campos_add['created_at'] = datos['created_at']
                campos_add['updated_at'] = datos['updated_at']

                venta_aumento_add = VentasAumentos.objects.create(**campos_add)
                venta_aumento_add.save()

                # detalles
                suma_subtotal = 0
                suma_total = 0
                for detalle in datos['detalles']:
                    suma_subtotal += detalle['total_salida']
                    suma_total += detalle['total_salida']
                    detalle_add = VentasAumentosDetalles.objects.create(venta_aumento_id=venta_aumento_add, venta_id=venta, punto_id=datos['punto_id'], producto_id=detalle['producto_id'],
                                                                        cantidad_salida=detalle['cantidad_salida'], costo_salida=detalle['costo_salida'], total_salida=detalle['total_salida'], detalle=detalle['detalle'])
                    detalle_add.save()

                    stock_up = stock_controller.update_stock(user_perfil=datos['user_perfil_id'], almacen=datos['almacen_id'], producto=detalle['producto_id'], cantidad=0-detalle['cantidad_salida'])
                    if not stock_up:
                        self.error_operation = 'Error al actualizar stock'
                        return False

                # actualizamos datos
                venta_aumento_add.subtotal = suma_subtotal
                venta_aumento_add.descuento = datos['descuento']
                venta_aumento_add.total = suma_total - datos['descuento'] + datos['costo_transporte']
                venta_aumento_add.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR registros add aumento, '+str(ex))
            return False

    def save_salida(self, **datos):
        """aniadimos a la base de datos"""
        try:
            if not self.permission_operation(datos['user_perfil_id'], datos['operation']):
                self.error_operation = 'no puede realizar esta operacion'
                return False

            venta = Ventas.objects.get(pk=datos['id'])
            if venta.status_id != self.status_venta:
                self.error_operation = 'esta operacion no es una venta'
                return False

            with transaction.atomic():
                campos_add = {}
                campos_add['user_perfil_id_salida'] = datos['user_perfil_id'].user_perfil_id
                campos_add['fecha_salida'] = datos['updated_at']
                campos_add['updated_at'] = datos['updated_at']
                campos_add['status_id'] = self.status_salida_almacen

                venta_actual = Ventas.objects.filter(pk=datos['id'])
                venta_actual.update(**campos_add)

                # todos los aumentos si es el caso
                venta = Ventas.objects.get(pk=datos['id'])
                ventas_aumentos = VentasAumentos.objects.filter(venta_id=venta, status_id=self.status_venta)
                for venta_aumento in ventas_aumentos:
                    venta_aumento.status_id = self.status_salida_almacen
                    venta_aumento.user_perfil_id_salida = datos['user_perfil_id'].user_perfil_id
                    venta_aumento.fecha_salida = datos['updated_at']
                    venta_aumento.updated_at = datos['updated_at']
                    venta_aumento.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR registros salida almacen, '+str(ex))
            return False

    def save_vuelta(self, **datos):
        """aniadimos a la base de datos"""
        stock_controller = StockController()
        try:
            if not self.permission_operation(datos['user_perfil_id'], datos['operation']):
                self.error_operation = 'no puede realizar esta operacion'
                return False

            venta = Ventas.objects.get(pk=datos['id'])
            if venta.status_id != self.status_salida_almacen:
                self.error_operation = 'esta operacion no es una salida de almacen'
                return False

            with transaction.atomic():
                campos_add = {}
                campos_add['user_perfil_id_vuelta'] = datos['user_perfil_id'].user_perfil_id
                campos_add['fecha_vuelta'] = datos['updated_at']
                campos_add['updated_at'] = datos['updated_at']
                campos_add['status_id'] = self.status_vuelta_almacen

                venta_actual = Ventas.objects.filter(pk=datos['id'])
                venta_actual.update(**campos_add)

                # todos los aumentos si es el caso
                venta = Ventas.objects.get(pk=datos['id'])
                # detalles
                for detalle in datos['detalles']:
                    # primero verificamos en las ventas detalles
                    up_ok = 0
                    detalle_up = VentasDetalles.objects.filter(venta_id=venta, producto_id=detalle['producto_id'])
                    if detalle_up:
                        detalle_act = detalle_up.first()
                        detalle_act.cantidad_vuelta = detalle['cantidad_vuelta']
                        detalle_act.costo_total_rotura = detalle['rotura']
                        detalle_act.costo_refaccion = detalle['refaccion']
                        detalle_act.total_vuelta_rotura = ((detalle['cantidad_salida'] - detalle_act.cantidad_vuelta) * detalle_act.costo_total_rotura) + detalle_act.costo_refaccion
                        detalle_act.save()
                        up_ok = 1
                    else:
                        # verificamos en los aumentos
                        ventas_aumentos = VentasAumentos.objects.filter(venta_id=venta, status_id=self.status_salida_almacen)
                        for venta_aumento in ventas_aumentos:
                            venta_aumentos_detalles = VentasAumentosDetalles.objects.filter(venta_aumento_id=venta_aumento, producto_id=detalle['producto_id'])
                            if venta_aumentos_detalles:
                                va_detalle = venta_aumentos_detalles.first()
                                va_detalle.cantidad_vuelta = detalle['cantidad_vuelta']
                                va_detalle.costo_total_rotura = detalle['rotura']
                                va_detalle.costo_refaccion = detalle['refaccion']
                                va_detalle.total_vuelta_rotura = ((detalle['cantidad_salida'] - va_detalle.cantidad_vuelta) * va_detalle.costo_total_rotura) + va_detalle.costo_refaccion
                                va_detalle.save()
                                up_ok = 1

                    if up_ok == 0:
                        self.error_operation = 'No existe el registro de detalle para este producto'
                        return False
                    else:
                        stock_up = stock_controller.update_stock(user_perfil=datos['user_perfil_id'], almacen=datos['almacen_id'], producto=detalle['producto_id'], cantidad=detalle['cantidad_vuelta'])
                        if not stock_up:
                            self.error_operation = 'Error al actualizar stock'
                            return False

                ventas_aumentos = VentasAumentos.objects.filter(venta_id=venta, status_id=self.status_salida_almacen)
                for venta_aumento in ventas_aumentos:
                    venta_aumento.status_id = self.status_vuelta_almacen
                    venta_aumento.user_perfil_id_vuelta = datos['user_perfil_id'].user_perfil_id
                    venta_aumento.fecha_salida = datos['updated_at']
                    venta_aumento.updated_at = datos['updated_at']
                    venta_aumento.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR registros salida almacen, '+str(ex))
            return False

    def save_finalizado(self, **datos):
        """aniadimos a la base de datos"""
        try:
            if not self.permission_operation(datos['user_perfil_id'], datos['operation']):
                self.error_operation = 'no puede realizar esta operacion'
                return False

            venta = Ventas.objects.get(pk=datos['id'])
            if venta.status_id != self.status_vuelta_almacen:
                self.error_operation = 'esta operacion no es una vuelta a almacen'
                return False

            with transaction.atomic():
                campos_add = {}
                campos_add['user_perfil_id_finaliza'] = datos['user_perfil_id'].user_perfil_id
                campos_add['fecha_finaliza'] = datos['updated_at']
                campos_add['updated_at'] = datos['updated_at']
                campos_add['status_id'] = self.status_finalizado

                venta_actual = Ventas.objects.filter(pk=datos['id'])
                venta_actual.update(**campos_add)

                # todos los aumentos si es el caso
                venta = Ventas.objects.get(pk=datos['id'])

                ventas_aumentos = VentasAumentos.objects.filter(venta_id=venta, status_id=self.status_vuelta_almacen)
                for venta_aumento in ventas_aumentos:
                    venta_aumento.status_id = self.status_finalizado
                    venta_aumento.user_perfil_id_finaliza = datos['user_perfil_id'].user_perfil_id
                    venta_aumento.fecha_finaliza = datos['updated_at']
                    venta_aumento.updated_at = datos['updated_at']
                    venta_aumento.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR registros salida almacen, '+str(ex))
            return False

    def add_gasto(self, venta_id, caja, request):
        try:
            caja_controller = CajasController()
            ce_controller = CajasEgresosController()
            user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
            punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)

            saldo_dia = caja_controller.day_balance(fecha=current_date(), Cajas=caja, formato_ori='yyyy-mm-dd')

            monto = validate_number_decimal('monto', request.POST['monto'])
            concepto = validate_string('concepto', request.POST['concepto'], remove_specials='yes')

            if monto > saldo_dia[caja.caja_id]:
                self.error_operation = 'El monto no debe ser mayor a ' + str(saldo_dia[caja.caja_id])
                return False

            # registramos el egreso de caja
            datos_egreso = {}
            datos_egreso['caja_id'] = caja
            datos_egreso['punto_id'] = punto
            datos_egreso['user_perfil_id'] = user_perfil
            datos_egreso['status_id'] = self.status_activo
            datos_egreso['fecha'] = get_date_to_db(fecha=current_date(), formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss')
            datos_egreso['concepto'] = concepto
            datos_egreso['monto'] = monto
            datos_egreso['venta_id'] = venta_id
            datos_egreso['created_at'] = 'now'
            datos_egreso['updated_at'] = 'now'

            if not ce_controller.add_db(**datos_egreso):
                self.error_operation = 'Error al registrar el gasto'
                return False

            self.error_operation = ''
            return True

        except Exception as ex:
            self.error_operation = 'Error de registro de gasto, ' + str(ex)
            return False

    def anular_gasto(self, venta_id, caja, request):
        try:
            ce_controller = CajasEgresosController()
            user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)

            motivo_anula = validate_string('motivo anula', request.POST['motivo_anula'], remove_specials='yes')
            ce_id = validate_number_int('caja egreso', request.POST['ce_id'])

            datos_egreso = {}
            datos_egreso['user_perfil_id_anula'] = user_perfil
            datos_egreso['status_id'] = self.status_anulado
            datos_egreso['motivo_anula'] = motivo_anula
            datos_egreso['deleted_at'] = 'now'

            if not ce_controller.delete_db(ce_id, **datos_egreso):
                self.error_operation = 'Error al anular el gasto'
                return False

            self.error_operation = ''
            return True

        except Exception as ex:
            self.error_operation = 'Error al anular el gasto, ' + str(ex)
            return False

    def add_cobro(self, venta_id, caja, request):
        try:
            caja_controller = CajasController()
            ci_controller = CajasIngresosController()
            user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
            punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)

            monto = validate_number_decimal('monto', request.POST['monto'])
            concepto = validate_string('concepto', request.POST['concepto'], remove_specials='yes')

            saldo_venta = self.saldo_venta(venta_id)
            if saldo_venta == -1000000:
                return False

            if monto > saldo_venta:
                self.error_operation = 'El saldo de la venta es ' + str(saldo_venta)
                return False

            # registramos el egreso de caja
            datos_ingreso = {}
            datos_ingreso['caja_id'] = caja
            datos_ingreso['punto_id'] = punto
            datos_ingreso['user_perfil_id'] = user_perfil
            datos_ingreso['status_id'] = self.status_activo
            datos_ingreso['fecha'] = get_date_to_db(fecha=current_date(), formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss')
            datos_ingreso['concepto'] = concepto
            datos_ingreso['monto'] = monto
            datos_ingreso['venta_id'] = venta_id
            datos_ingreso['created_at'] = 'now'
            datos_ingreso['updated_at'] = 'now'

            if not ci_controller.add_db(**datos_ingreso):
                self.error_operation = 'Error al registrar el cobro'
                return False

            self.error_operation = ''
            return True

        except Exception as ex:
            self.error_operation = 'Error de registro de cobro, ' + str(ex)
            return False

    def saldo_venta(self, venta_id):
        try:
            venta = Ventas.objects.get(pk=venta_id)
            saldo_venta = venta.total
            saldo_venta = saldo_venta + venta.garantia_bs

            # lista de gastos
            lista_gastos = apps.get_model('cajas', 'CajasEgresos').objects.filter(venta_id=venta.venta_id, status_id=self.status_activo).order_by('caja_egreso_id')
            lista_ingresos = apps.get_model('cajas', 'CajasIngresos').objects.filter(venta_id=venta.venta_id, status_id=self.status_activo).order_by('caja_ingreso_id')

            for gasto in lista_gastos:
                saldo_venta = saldo_venta + gasto.monto

            for ingreso in lista_ingresos:
                saldo_venta = saldo_venta - ingreso.monto

            # devolucion de productos y aumentos
            ventas_detalles = VentasDetalles.objects.filter(venta_id=venta)
            deuda_detalles = 0
            for detalle in ventas_detalles:
                deuda_detalles += detalle.total_vuelta_rotura

            # aumentos
            filtro_aumento = {}
            filtro_aumento['venta_id'] = venta
            filtro_aumento['status_id__in'] = [self.status_venta, self.status_salida_almacen, self.status_vuelta_almacen]
            ventas_aumentos = VentasAumentos.objects.filter(**filtro_aumento)
            for ve_aumento in ventas_aumentos:
                ventas_aumentos_detalles = VentasAumentosDetalles.objects.filter(venta_aumento_id=ve_aumento)
                for detalle in ventas_aumentos_detalles:
                    deuda_detalles += detalle.total_vuelta_rotura

            saldo_venta = saldo_venta + deuda_detalles - venta.garantia_bs

            return saldo_venta
            #self.error_operation = 'saldo venta: ' + str(saldo_venta)
            # return False
        except Exception as ex:
            self.error_operation = 'Error al recuperar el saldo de la venta'
            return -1000000

    def anular_cobro(self, venta_id, caja, request):
        try:
            ci_controller = CajasIngresosController()
            user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)

            motivo_anula = validate_string('motivo anula', request.POST['motivo_anula'], remove_specials='yes')
            ci_id = validate_number_int('caja ingreso', request.POST['ci_id'])

            datos_ingreso = {}
            datos_ingreso['user_perfil_id_anula'] = user_perfil
            datos_ingreso['status_id'] = self.status_anulado
            datos_ingreso['motivo_anula'] = motivo_anula
            datos_ingreso['deleted_at'] = 'now'

            if not ci_controller.delete_db(ci_id, **datos_ingreso):
                self.error_operation = 'Error al anular el cobro'
                return False

            self.error_operation = ''
            return True

        except Exception as ex:
            self.error_operation = 'Error al anular el cobro, ' + str(ex)
            return False

    def can_anular(self, id, usuario_perfil):
        """verificando si se puede eliminar o no la tabla"""
        try:
            # puede anular el usuario con permiso de la sucursal
            venta = apps.get_model('ventas', 'Ventas').objects.get(pk=id)
            #print('venta: ', venta.status_id.status_id, ' self: ', self.venta)
            permisos = get_permissions_user(usuario_perfil.user_id, settings.MOD_VENTAS)

            venta = Ventas.objects.get(pk=id)
            if venta.status_id.status_id == self.anulado:
                self.error_operation = 'el registro ya esta anulado'
                return False

            if not self.permission_operation(usuario_perfil, 'anular'):
                self.error_operation = 'no tiene permiso para anular este registro'
                return False

            if venta.status_id.status_id == self.venta:
                # verificamos que no tenga aumentos activos
                ventas_aumentos = VentasAumentos.objects.filter(venta_id=venta, status_id=self.status_venta).count()
                if ventas_aumentos > 0:
                    self.error_operation = 'primero debe anular los aumentos de esta venta'
                    return False

                # verificamos cobros y gastos
                cant_gastos = apps.get_model('cajas', 'CajasEgresos').objects.filter(venta_id=venta, status_id=self.status_activo).count()
                if cant_gastos > 0:
                    self.error_operation = 'primero debe anular los gastos de esta venta'
                    return False

                cant_ingresos = apps.get_model('cajas', 'CajasIngresos').objects.filter(venta_id=venta, status_id=self.status_activo).count()
                if cant_ingresos > 0:
                    self.error_operation = 'primero debe anular los ingresos de esta venta'
                    return False

            if permisos.anular:
                return True

            return False

        except Exception as ex:
            print('error can anular: ', str(ex))
            return False

    def anular(self, request, id):
        """anulando el registro"""
        try:
            usuario_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
            if self.can_anular(id, usuario_perfil):

                status_anular = self.status_anulado
                operation = validate_number_int('operation', request.POST['operation'], len_zero='yes')
                if operation == self.preventa:
                    motivo_a = ''
                else:
                    motivo_a = validate_string('motivo anula', request.POST['motivo_anula'], remove_specials='yes')

                campos_update = {}
                # para actualizar el stock
                almacen_id = 1
                almacen = Almacenes.objects.get(pk=almacen_id)
                campos_update['almacen_id'] = almacen
                campos_update['user_perfil_id'] = usuario_perfil
                campos_update['user_perfil_id_anula'] = usuario_perfil.user_perfil_id
                campos_update['motivo_anula'] = motivo_a
                campos_update['operation'] = operation
                campos_update['status_id'] = status_anular
                campos_update['deleted_at'] = 'now'

                if self.anular_db(id, **campos_update):
                    self.error_operation = ''
                    return True
                else:
                    return False

            else:
                self.error_operation = 'No tiene permiso para anular este registro'
                return False

        except Exception as ex:
            print('Error anular ingreso almacen: ' + str(ex))
            self.error_operation = 'Error al anular el registro, ' + str(ex)
            return False

    def anular_aumento(self, request, vaid):
        """anulando el registro"""

        try:
            usuario_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
            venta_aumento = VentasAumentos.objects.get(pk=int(vaid))
            # if self.can_anular(venta_aumento.venta_id.venta_id, usuario_perfil):
            #print('venta aumento...: ', venta_aumento)
            if venta_aumento.status_id == self.status_venta:

                status_anular = self.status_anulado
                motivo_a = validate_string('motivo anula', request.POST['motivo_anula'], remove_specials='yes')

                campos_update = {}
                # para actualizar el stock
                almacen_id = 1
                almacen = Almacenes.objects.get(pk=almacen_id)
                campos_update['almacen_id'] = almacen
                campos_update['user_perfil_id'] = usuario_perfil
                campos_update['user_perfil_id_anula'] = usuario_perfil.user_perfil_id
                campos_update['motivo_anula'] = motivo_a
                campos_update['status_id'] = status_anular
                campos_update['deleted_at'] = 'now'

                if self.anular_aumento_db(vaid, **campos_update):
                    self.error_operation = ''
                    return True
                else:
                    return False

            else:
                self.error_operation = 'No tiene permiso para anular este registro'
                return False

        except Exception as ex:
            print('Error anular aumento: ' + str(ex))
            self.error_operation = 'Error al anular el registro, ' + str(ex)
            return False

    def anular_db(self, id, **datos):
        """ anulamos en la bd """
        stock_controller = StockController()
        try:
            if self.can_anular(id, datos['user_perfil_id']):
                with transaction.atomic():
                    if datos['operation'] == self.preventa:
                        campos_update = {}
                        campos_update['user_perfil_id_anula'] = datos['user_perfil_id_anula']
                        campos_update['motivo_anula'] = datos['motivo_anula']
                        campos_update['status_id'] = datos['status_id']
                        campos_update['deleted_at'] = datos['deleted_at']

                        # registramos
                        venta_update = Ventas.objects.filter(pk=id)
                        venta_update.update(**campos_update)

                        self.error_operation = ''
                        return True

                    if datos['operation'] == self.venta:
                        campos_update = {}
                        campos_update['user_perfil_id_anula'] = datos['user_perfil_id_anula']
                        campos_update['motivo_anula'] = datos['motivo_anula']
                        campos_update['status_id'] = self.status_preventa
                        campos_update['updated_at'] = datos['deleted_at']

                        # registramos
                        venta_update = Ventas.objects.filter(pk=id)
                        venta_update.update(**campos_update)

                        # detalles
                        venta = Ventas.objects.get(pk=id)
                        venta_detalles = VentasDetalles.objects.filter(venta_id=venta)
                        for detalle in venta_detalles:
                            # actualizamos el stock
                            stock_up = stock_controller.update_stock(user_perfil=datos['user_perfil_id'], almacen=datos['almacen_id'], producto=detalle.producto_id, cantidad=detalle.cantidad_salida)
                            if not stock_up:
                                self.error_operation = 'Error al actualizar stock'
                                return False

                        self.error_operation = ''
                        return True

                    if datos['operation'] == self.salida_almacen:
                        campos_update = {}
                        campos_update['user_perfil_id_anula'] = datos['user_perfil_id_anula']
                        campos_update['motivo_anula'] = datos['motivo_anula']
                        campos_update['status_id'] = self.status_venta
                        campos_update['updated_at'] = datos['deleted_at']

                        # registramos
                        venta_update = Ventas.objects.filter(pk=id)
                        venta_update.update(**campos_update)

                        # todos los aumentos si es el caso
                        venta = Ventas.objects.get(pk=id)
                        ventas_aumentos = VentasAumentos.objects.filter(venta_id=venta, status_id=self.status_salida_almacen)
                        for venta_aumento in ventas_aumentos:
                            venta_aumento.status_id = self.status_venta
                            venta_aumento.updated_at = datos['deleted_at']
                            venta_aumento.save()

                        self.error_operation = ''
                        return True

                    if datos['operation'] == self.vuelta_almacen:
                        campos_update = {}
                        campos_update['user_perfil_id_anula'] = datos['user_perfil_id_anula']
                        campos_update['motivo_anula'] = datos['motivo_anula']
                        campos_update['status_id'] = self.status_salida_almacen
                        campos_update['updated_at'] = datos['deleted_at']

                        # registramos
                        venta_update = Ventas.objects.filter(pk=id)
                        venta_update.update(**campos_update)

                        # todos los aumentos si es el caso
                        venta = Ventas.objects.get(pk=id)
                        # detalles y stock
                        ventas_detalles = VentasDetalles.objects.filter(venta_id=venta)
                        for venta_detalle in ventas_detalles:
                            # actualizamos el stock si es el caso
                            if venta_detalle.cantidad_vuelta > 0:
                                stock_up = stock_controller.update_stock(user_perfil=datos['user_perfil_id'], almacen=datos['almacen_id'], producto=venta_detalle.producto_id, cantidad=0-venta_detalle.cantidad_vuelta)
                                if not stock_up:
                                    self.error_operation = 'Error al actualizar stock'
                                    return False

                            venta_detalle.cantidad_vuelta = 0
                            venta_detalle.costo_total_rotura = 0
                            venta_detalle.costo_refaccion = 0
                            venta_detalle.total_vuelta_rotura = 0
                            venta_detalle.save()

                        ventas_aumentos = VentasAumentos.objects.filter(venta_id=venta, status_id=self.status_vuelta_almacen)
                        for venta_aumento in ventas_aumentos:
                            venta_aumento.status_id = self.status_salida_almacen
                            venta_aumento.updated_at = datos['deleted_at']
                            venta_aumento.save()

                            ventas_aumentos_detalles = VentasAumentosDetalles.objects.filter(venta_aumento_id=venta_aumento)
                            for va_detalle in ventas_aumentos_detalles:
                                # actualizamos el stock si es el caso
                                if va_detalle.cantidad_vuelta > 0:
                                    stock_up = stock_controller.update_stock(user_perfil=datos['user_perfil_id'], almacen=datos['almacen_id'], producto=va_detalle.producto_id, cantidad=0-va_detalle.cantidad_vuelta)
                                    if not stock_up:
                                        self.error_operation = 'Error al actualizar stock'
                                        return False

                                va_detalle.cantidad_vuelta = 0
                                va_detalle.costo_total_rotura = 0
                                va_detalle.costo_refaccion = 0
                                va_detalle.total_vuelta_rotura = 0
                                va_detalle.save()

                        self.error_operation = ''
                        return True

                    if datos['operation'] == self.finalizado:
                        campos_update = {}
                        campos_update['user_perfil_id_anula'] = datos['user_perfil_id_anula']
                        campos_update['motivo_anula'] = datos['motivo_anula']
                        campos_update['status_id'] = self.status_vuelta_almacen
                        campos_update['updated_at'] = datos['deleted_at']

                        # registramos
                        venta_update = Ventas.objects.filter(pk=id)
                        venta_update.update(**campos_update)

                        # todos los aumentos si es el caso
                        venta = Ventas.objects.get(pk=id)

                        ventas_aumentos = VentasAumentos.objects.filter(venta_id=venta, status_id=self.status_finalizado)
                        for venta_aumento in ventas_aumentos:
                            venta_aumento.status_id = self.status_vuelta_almacen
                            venta_aumento.updated_at = datos['deleted_at']
                            venta_aumento.save()

                        self.error_operation = ''
                        return True

                    self.error_operation = 'operation no valid'
                    return False
            else:
                self.error_operation = 'No tiene permiso para anular este registro'
                return False

        except Exception as ex:
            print('Error anular venta db: ' + str(ex))
            self.error_operation = 'Error de argumentos, ' + str(ex)
            return False

    def anular_aumento_db(self, vaid, **datos):
        """ anulamos en la bd """
        stock_controller = StockController()
        try:
            venta_aumento = VentasAumentos.objects.get(pk=vaid)
            # if self.can_anular(venta_aumento.venta_id.venta_id, datos['user_perfil_id']):
            if venta_aumento.status_id == self.status_venta:
                with transaction.atomic():

                    campos_update = {}
                    campos_update['user_perfil_id_anula'] = datos['user_perfil_id_anula']
                    campos_update['motivo_anula'] = datos['motivo_anula']
                    campos_update['status_id'] = datos['status_id']
                    campos_update['deleted_at'] = datos['deleted_at']

                    # registramos
                    venta_update = VentasAumentos.objects.filter(pk=vaid)
                    venta_update.update(**campos_update)

                    # detalles
                    venta_aumento = VentasAumentos.objects.get(pk=vaid)
                    venta_aumento_detalles = VentasAumentosDetalles.objects.filter(venta_aumento_id=venta_aumento)
                    for detalle in venta_aumento_detalles:
                        # actualizamos el stock
                        stock_up = stock_controller.update_stock(user_perfil=datos['user_perfil_id'], almacen=datos['almacen_id'], producto=detalle.producto_id, cantidad=detalle.cantidad_salida)
                        if not stock_up:
                            self.error_operation = 'Error al actualizar stock'
                            return False

                    self.error_operation = ''
                    return True

            else:
                self.error_operation = 'No tiene permiso para anular este registro'
                return False

        except Exception as ex:
            print('Error anular aumento db: ' + str(ex))
            self.error_operation = 'Error de argumentos, ' + str(ex)
            return False

    def stock_productos(self, fecha_entrega, fecha_devolucion, formato='yyyy-mm-dd HH:ii:ss', ventas_not_in=''):
        lista_stock = {}

        configuraciones_sistema = get_system_settings()
        minutos_antes_devolucion = configuraciones_sistema['minutos_antes_devolucion']
        minutos_despues_entrega = configuraciones_sistema['minutos_despues_entrega']

        fecha_ini = add_minutes_datetime(fecha=get_date_to_db(fecha=fecha_entrega, formato_ori=formato, formato='yyyy-mm-dd HH:ii:ss'), minutos_add=0-minutos_antes_devolucion)
        fecha_fin = add_minutes_datetime(fecha=get_date_to_db(fecha=fecha_devolucion, formato_ori=formato, formato='yyyy-mm-dd HH:ii:ss'), minutos_add=minutos_despues_entrega)
        #print('vc fecha ini: ', fecha_ini, ' vc fecha fin: ', fecha_fin)
        fecha_ini_int = get_fecha_int(fecha_ini)
        fecha_fin_int = get_fecha_int(fecha_fin)
        #print('ini int: ', fecha_ini_int, ' fin int: ', fecha_fin_int)

        # todos los productos con stock
        #sql = f"SELECT p.producto_id FROM productos p WHERE p.status_id='{self.activo}' "
        sql = f"SELECT p.producto_id FROM productos p "
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                lista_stock[row[0]] = 0

        # tabla stock de productos
        sql = "SELECT cantidad, producto_id FROM stock WHERE almacen_id='1' "
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                existe = lista_stock.get(row[1], 'sinvalor')
                if existe == 'sinvalor':
                    lista_stock[row[1]] = 0
                else:
                    lista_stock[row[1]] += int(row[0])

        #print('lista stock: ', lista_stock)
        # recuperamos todas las ventas, estado venta y salida de almacen
        sql_add = ''
        if ventas_not_in != '':
            sql_add = f"AND v.venta_id NOT IN({ventas_not_in}) "

        # sql = "SELECT v.venta_id, vad.venta_aumento_detalle_id, v.fecha_entrega, v.fecha_devolucion, vd.producto_id, vd.cantidad_salida, "
        # sql += "vad.producto_id, vad.cantidad_salida "
        # sql += "FROM ventas v INNER JOIN ventas_detalles vd ON v.venta_id=vd.venta_id "
        # sql += "LEFT JOIN ventas_aumentos_detalles vad ON v.venta_id=vad.venta_id "
        # sql += f"WHERE v.status_id IN ('{self.venta}', '{self.salida_almacen}') " + sql_add
        # sql += "ORDER BY v.fecha_entrega "

        sql = "SELECT v.venta_id, 'VENTAS' AS tipo, vd.venta_detalle_id, v.fecha_entrega, v.fecha_devolucion, "
        sql += "vd.producto_id, vd.cantidad_salida "
        sql += "FROM ventas v INNER JOIN ventas_detalles vd ON v.venta_id=vd.venta_id "
        sql += f"WHERE v.status_id IN ('{self.venta}', '{self.salida_almacen}') " + sql_add
        sql += "UNION "
        sql += "SELECT v.venta_id, 'AUMENTOS' AS tipo, vad.venta_aumento_detalle_id AS venta_detalle_id, v.fecha_entrega, v.fecha_devolucion, "
        sql += "vad.producto_id, vad.cantidad_salida "
        sql += "FROM ventas v, ventas_aumentos va, ventas_aumentos_detalles vad "
        sql += "WHERE v.venta_id=va.venta_id AND va.venta_aumento_id=vad.venta_aumento_id "
        sql += f"AND v.status_id IN ('{self.venta}', '{self.salida_almacen}') AND va.status_id != '{self.anulado}' "

        # print(sql)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                tipo_venta = row[1]
                fecha_entrega = row[3]
                fecha_devolucion = row[4]
                fecha_entrega_int = get_fecha_int(fecha_entrega)
                fecha_devolucion_int = get_fecha_int(fecha_devolucion)

                producto_id = row[5]
                cantidad_salida = int(row[6])

                # # comparamos fechas
                # # aumentamos las ventas que llegaran "minutos_antes_devolucion" de la fecha de entrega
                # if fecha_devolucion_int <= fecha_ini_int:
                #     # los pedidos llegaran en la fecha mas el tiempo permitido de "minutos_antes_devolucion"
                #     lista_stock[producto_id] += cantidad_salida

                # # quitamos del stock si el producto saldra entre la fecha inicial y la fecha final
                # if fecha_entrega_int >= fecha_ini_int and fecha_entrega_int <= fecha_fin_int:
                #     lista_stock[producto_id] -= cantidad_salida

                # aumentos
                if fecha_entrega_int <= fecha_ini_int and fecha_entrega_int <= fecha_fin_int and fecha_devolucion_int <= fecha_ini_int and fecha_devolucion_int <= fecha_fin_int:
                    # print('aumento 1: ', fecha_entrega_int, ' <= ', fecha_ini_int, ' and ', fecha_entrega_int, ' <= ', fecha_fin_int,
                    #       ' and ', fecha_devolucion_int, ' <= ', fecha_ini_int, ' and ', fecha_devolucion_int, ' <= ', fecha_fin_int)
                    lista_stock[producto_id] += cantidad_salida

                elif fecha_entrega_int >= fecha_ini_int and fecha_entrega_int >= fecha_fin_int and fecha_devolucion_int >= fecha_ini_int and fecha_devolucion_int >= fecha_fin_int:
                    # print('aumento 2: ', fecha_entrega_int, ' >= ', fecha_ini_int, ' and ', fecha_entrega_int, ' >= ', fecha_fin_int,
                    #       ' and ', fecha_devolucion_int, ' >= ', fecha_ini_int, ' and ', fecha_devolucion_int, ' >= ', fecha_fin_int)
                    lista_stock[producto_id] += cantidad_salida

                # resta
                elif fecha_entrega_int <= fecha_ini_int and fecha_entrega_int <= fecha_fin_int and fecha_devolucion_int >= fecha_ini_int and fecha_devolucion_int <= fecha_fin_int:
                    # print('resta 1: ', fecha_entrega_int, ' <= ', fecha_ini_int, ' and ', fecha_entrega_int, ' <= ', fecha_fin_int,
                    #       ' and ', fecha_devolucion_int, ' >= ', fecha_ini_int, ' and ', fecha_devolucion_int, ' <= ', fecha_fin_int)
                    lista_stock[producto_id] -= cantidad_salida

                elif fecha_entrega_int <= fecha_ini_int and fecha_entrega_int <= fecha_fin_int and fecha_devolucion_int >= fecha_ini_int and fecha_devolucion_int >= fecha_fin_int:
                    # print('resta 2: ', fecha_entrega_int, ' <= ', fecha_ini_int, ' and ', fecha_entrega_int, ' <= ', fecha_fin_int,
                    #       ' and ', fecha_devolucion_int, ' >= ', fecha_ini_int, ' and ', fecha_devolucion_int, ' >= ', fecha_fin_int)
                    lista_stock[producto_id] -= cantidad_salida

                elif fecha_entrega_int >= fecha_ini_int and fecha_entrega_int <= fecha_fin_int and fecha_devolucion_int >= fecha_ini_int and fecha_devolucion_int <= fecha_fin_int:
                    # print('resta 3: ', fecha_entrega_int, ' >= ', fecha_ini_int, ' and ', fecha_entrega_int, ' <= ', fecha_fin_int,
                    #       ' and ', fecha_devolucion_int, ' >= ', fecha_ini_int, ' and ', fecha_devolucion_int, ' <= ', fecha_fin_int)
                    lista_stock[producto_id] -= cantidad_salida

                elif fecha_entrega_int >= fecha_ini_int and fecha_entrega_int <= fecha_fin_int and fecha_devolucion_int >= fecha_ini_int and fecha_devolucion_int >= fecha_fin_int:
                    # print('resta 4: ', fecha_entrega_int, ' >= ', fecha_ini_int, ' and ', fecha_entrega_int, ' <= ', fecha_fin_int,
                    #       ' and ', fecha_devolucion_int, ' >= ', fecha_ini_int, ' and ', fecha_devolucion_int, ' >= ', fecha_fin_int)
                    lista_stock[producto_id] -= cantidad_salida

        return lista_stock
