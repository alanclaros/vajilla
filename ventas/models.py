from django.db import models

from status.models import Status
from utils.custome_db_types import DateTimeFieldCustome
from configuraciones.models import Puntos, Almacenes
from permisos.models import UsersPerfiles
from productos.models import Productos
from clientes.models import Clientes


class Ventas(models.Model):
    venta_id = models.AutoField(primary_key=True, db_column='venta_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    almacen_id = models.ForeignKey(Almacenes, to_field='almacen_id', on_delete=models.PROTECT, db_column='almacen_id')
    cliente_id = models.ForeignKey(Clientes, to_field='cliente_id', on_delete=models.PROTECT, db_column='cliente_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    apellidos = models.CharField(max_length=150, blank=False, null=False, default='')
    nombres = models.CharField(max_length=150, blank=False, null=False, default='')
    ci_nit = models.CharField(max_length=150, blank=False, null=False, default='')
    telefonos = models.CharField(max_length=150, blank=False, null=False, default='')
    factura_a = models.CharField(max_length=150, blank=False, null=False, default='')
    numero_contrato = models.CharField(max_length=50, blank=False, null=False, default='')

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo_transporte = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    garantia = models.CharField(max_length=250, blank=False, null=False, default='')
    garantia_bs = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    direccion_evento = models.TextField(blank=False, null=False, default='')
    observacion = models.TextField(blank=False, null=False, default='')

    fecha_entrega = DateTimeFieldCustome(null=True, blank=True)
    fecha_devolucion = DateTimeFieldCustome(null=True, blank=True)
    fecha_evento = DateTimeFieldCustome(null=True, blank=True)

    dias = models.IntegerField(blank=False, null=False, default=0)
    fecha_preventa = DateTimeFieldCustome(null=True, blank=True)
    user_perfil_id_preventa = models.IntegerField(blank=False, null=False, default=0)
    fecha_venta = DateTimeFieldCustome(null=True, blank=True)
    user_perfil_id_venta = models.IntegerField(blank=False, null=False, default=0)
    fecha_salida = DateTimeFieldCustome(null=True, blank=True)
    user_perfil_id_salida = models.IntegerField(blank=False, null=False, default=0)
    fecha_vuelta = DateTimeFieldCustome(null=True, blank=True)
    user_perfil_id_vuelta = models.IntegerField(blank=False, null=False, default=0)
    fecha_finaliza = DateTimeFieldCustome(null=True, blank=True)
    user_perfil_id_finaliza = models.IntegerField(blank=False, null=False, default=0)

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'ventas'


class VentasDetalles(models.Model):
    venta_detalle_id = models.AutoField(primary_key=True, db_column='venta_detalle_id')
    venta_id = models.ForeignKey(Ventas, to_field='venta_id', on_delete=models.PROTECT, db_column='venta_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')

    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')
    cantidad_salida = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo_salida = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total_salida = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    cantidad_vuelta = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo_total_rotura = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo_refaccion = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total_vuelta_rotura = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    detalle = models.CharField(max_length=250, blank=False, null=False, default='')

    class Meta:
        db_table = 'ventas_detalles'


class VentasAumentos(models.Model):
    venta_aumento_id = models.AutoField(primary_key=True, db_column='venta_aumento_id')
    venta_id = models.ForeignKey(Ventas, to_field='venta_id', on_delete=models.PROTECT, db_column='venta_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo_transporte = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    garantia = models.CharField(max_length=250, blank=False, null=False, default='')
    garantia_bs = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    observacion = models.TextField(blank=False, null=False, default='')

    fecha_salida = DateTimeFieldCustome(null=True, blank=True)
    user_perfil_id_salida = models.IntegerField(blank=False, null=False, default=0)
    fecha_vuelta = DateTimeFieldCustome(null=True, blank=True)
    user_perfil_id_vuelta = models.IntegerField(blank=False, null=False, default=0)
    fecha_finaliza = DateTimeFieldCustome(null=True, blank=True)
    user_perfil_id_finaliza = models.IntegerField(blank=False, null=False, default=0)

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'ventas_aumentos'


class VentasAumentosDetalles(models.Model):
    venta_aumento_detalle_id = models.AutoField(primary_key=True, db_column='venta_aumento_detalle_id')
    venta_aumento_id = models.ForeignKey(VentasAumentos, to_field='venta_aumento_id', on_delete=models.PROTECT, db_column='venta_aumento_id')
    venta_id = models.ForeignKey(Ventas, to_field='venta_id', on_delete=models.PROTECT, db_column='venta_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')

    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')
    cantidad_salida = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo_salida = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total_salida = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    cantidad_vuelta = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo_total_rotura = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo_refaccion = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total_vuelta_rotura = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    detalle = models.CharField(max_length=250, blank=False, null=False, default='')

    class Meta:
        db_table = 'ventas_aumentos_detalles'
