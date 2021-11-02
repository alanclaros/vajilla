from django.db import models
from status.models import Status
from configuraciones.models import Puntos, Cajas, Monedas, TiposMonedas
from permisos.models import UsersPerfiles
from utils.custome_db_types import DateTimeFieldCustome, DateFieldCustome
from django.conf import settings


class CajasIngresos(models.Model):
    caja_ingreso_id = models.AutoField(primary_key=True, db_column='caja_ingreso_id')
    caja_id = models.ForeignKey(Cajas, to_field='caja_id', on_delete=models.PROTECT, db_column='caja_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    venta_id = models.IntegerField(blank=False, null=False, default=0)
    caja_movimiento_id = models.IntegerField(blank=False, null=False, default=0)
    es_garantia = models.IntegerField(blank=False, null=False, default=0)

    fecha = DateTimeFieldCustome(null=True, blank=True)
    concepto = models.CharField(max_length=250, blank=False)
    monto = models.DecimalField(max_digits=12, decimal_places=2, blank=False, default=0)
    user_perfil_id_anula = models.IntegerField(null=True, blank=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)

    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'cajas_ingresos'


class CajasEgresos(models.Model):
    caja_egreso_id = models.AutoField(primary_key=True, db_column='caja_egreso_id')
    caja_id = models.ForeignKey(Cajas, to_field='caja_id', on_delete=models.PROTECT, db_column='caja_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    venta_id = models.IntegerField(blank=False, null=False, default=0)
    caja_movimiento_id = models.IntegerField(blank=False, null=False, default=0)
    es_garantia = models.IntegerField(blank=False, null=False, default=0)

    fecha = DateTimeFieldCustome(null=True, blank=True)
    concepto = models.CharField(max_length=250, blank=False)
    monto = models.DecimalField(max_digits=12, decimal_places=2, blank=False, default=0)
    user_perfil_id_anula = models.IntegerField(null=True)
    motivo_anula = models.CharField(max_length=250, null=True)

    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'cajas_egresos'


class CajasOperaciones(models.Model):
    caja_operacion_id = models.AutoField(primary_key=True, db_column='caja_operacion_id')
    caja_id = models.ForeignKey(Cajas, to_field='caja_id', on_delete=models.PROTECT, db_column='caja_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    fecha = DateFieldCustome(null=True, blank=True)
    monto_apertura = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    monto_cierre = models.DecimalField(max_digits=12, decimal_places=2, blank=False)

    usuario_perfil_apertura_id = models.IntegerField(blank=False)
    usuario_perfil_apertura_r_id = models.IntegerField(blank=False)
    usuario_perfil_cierre_id = models.IntegerField(blank=False)
    usuario_perfil_cierre_r_id = models.IntegerField(blank=False)

    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'cajas_operaciones'


class CajasOperacionesDetalles(models.Model):
    caja_operacion_detalle_id = models.AutoField(primary_key=True, db_column='caja_operacion_detalle_id')
    caja_operacion_id = models.ForeignKey(CajasOperaciones, to_field='caja_operacion_id', on_delete=models.PROTECT, db_column='caja_operacion_id')
    moneda_id = models.ForeignKey(Monedas, to_field='moneda_id', on_delete=models.PROTECT, db_column='moneda_id')
    cantidad_apertura = models.IntegerField(blank=False)
    cantidad_cierre = models.IntegerField(blank=False)

    class Meta:
        db_table = 'cajas_operaciones_detalles'


class CajasMovimientos(models.Model):
    caja_movimiento_id = models.AutoField(primary_key=True, db_column='caja_movimiento_id')
    caja1_id = models.ForeignKey(Cajas, verbose_name='caja1', related_name='primera_caja', on_delete=models.PROTECT, db_column='caja1_id', to_field='caja_id')
    caja2_id = models.ForeignKey(Cajas, verbose_name='caja2', related_name='segunda_caja', on_delete=models.PROTECT, db_column='caja2_id', to_field='caja_id')

    caja1_user_perfil_id = models.ForeignKey(UsersPerfiles, verbose_name='usuario1', related_name='primer_usuario', on_delete=models.PROTECT, db_column='caja1_user_perfil_id', to_field='user_perfil_id')
    caja2_user_perfil_id = models.ForeignKey(UsersPerfiles, verbose_name='usuario2', related_name='segundo_usuario', on_delete=models.PROTECT, db_column='caja2_user_perfil_id', to_field='user_perfil_id')

    tipo_moneda_id = models.ForeignKey(TiposMonedas, to_field='tipo_moneda_id', on_delete=models.PROTECT, db_column='tipo_moneda_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    fecha = DateTimeFieldCustome(null=True, blank=True)
    concepto = models.CharField(max_length=250, blank=False)
    monto = models.DecimalField(max_digits=12, decimal_places=2, blank=False, default=0)
    user_perfil_id_anula = models.IntegerField(null=True, blank=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)

    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'cajas_movimientos'
