from django.db import models

from status.models import Status
from permisos.models import UsersPerfiles
from utils.custome_db_types import DateFieldCustome, DateTimeFieldCustome


class Configuraciones(models.Model):
    configuracion_id = models.IntegerField(primary_key=True)
    cant_per_page = models.IntegerField(blank=False, null=False)
    usar_fecha_servidor = models.CharField(max_length=20, blank=False, null=False, default='si')
    fecha_sistema = DateFieldCustome(null=True, blank=True)
    minutos_antes_devolucion = models.IntegerField(blank=False, null=False)
    minutos_despues_entrega = models.IntegerField(blank=False, null=False)

    class Meta:
        db_table = 'configuraciones'


class Paises(models.Model):
    pais_id = models.IntegerField(primary_key=True, db_column='pais_id')
    pais = models.CharField(max_length=150, blank=False)

    class Meta:
        db_table = 'paises'


class Ciudades(models.Model):
    ciudad_id = models.AutoField(primary_key=True, db_column='ciudad_id')
    pais_id = models.ForeignKey(Paises, to_field='pais_id', on_delete=models.PROTECT, db_column='pais_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    ciudad = models.CharField(max_length=150, blank=False)
    codigo = models.CharField(max_length=50, blank=False)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'ciudades'


class Sucursales(models.Model):
    sucursal_id = models.AutoField(primary_key=True, db_column='sucursal_id')
    ciudad_id = models.ForeignKey(Ciudades, to_field='ciudad_id', on_delete=models.PROTECT, db_column='ciudad_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    sucursal = models.CharField(max_length=250, blank=False)
    codigo = models.CharField(max_length=50, blank=False)
    email = models.CharField(max_length=250, blank=False)
    empresa = models.CharField(max_length=250, blank=False)
    direccion = models.CharField(max_length=250, blank=False)
    ciudad = models.CharField(max_length=250, blank=False)
    telefonos = models.CharField(max_length=250, blank=False)
    actividad = models.CharField(max_length=250, blank=False)

    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'sucursales'


class Puntos(models.Model):
    punto_id = models.AutoField(primary_key=True, db_column='punto_id')
    sucursal_id = models.ForeignKey(Sucursales, to_field='sucursal_id', on_delete=models.PROTECT, db_column='sucursal_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    punto = models.CharField(max_length=150, blank=False)
    codigo = models.CharField(max_length=50, blank=False)
    impresora_reportes = models.CharField(max_length=250, blank=False)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'puntos'


class TiposMonedas(models.Model):
    tipo_moneda_id = models.IntegerField(primary_key=True, db_column='tipo_moneda_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    tipo_moneda = models.CharField(max_length=150, blank=False)
    codigo = models.CharField(max_length=50, blank=False)

    class Meta:
        db_table = 'tipos_monedas'


class Monedas(models.Model):
    moneda_id = models.IntegerField(primary_key=True, db_column='moneda_id')
    tipo_moneda_id = models.ForeignKey(TiposMonedas, to_field='tipo_moneda_id', on_delete=models.PROTECT, db_column='tipo_moneda_id')
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    class Meta:
        db_table = 'monedas'


class Cajas(models.Model):
    caja_id = models.AutoField(primary_key=True, db_column='caja_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    tipo_moneda_id = models.ForeignKey(TiposMonedas, to_field='tipo_moneda_id', on_delete=models.PROTECT, db_column='tipo_moneda_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    caja = models.CharField(max_length=150, blank=False)
    codigo = models.CharField(max_length=50, blank=False)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'cajas'


class Almacenes(models.Model):
    almacen_id = models.AutoField(primary_key=True, db_column='almacen_id')
    almacen = models.CharField(max_length=150, blank=False, null=False, default='')
    codigo = models.CharField(max_length=20, blank=False, null=False, default='')
    sucursal_id = models.ForeignKey(Sucursales, to_field='sucursal_id', on_delete=models.PROTECT, db_column='sucursal_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'almacenes'


class Lineas(models.Model):
    linea_id = models.AutoField(primary_key=True, db_column='linea_id')
    linea = models.CharField(max_length=150, blank=False, null=False, default='')
    codigo = models.CharField(max_length=150, blank=False, null=False, default='')
    linea_principal = models.IntegerField(blank=False, null=False, default=0)
    linea_superior_id = models.IntegerField(blank=False, null=False, default=0)
    descripcion = models.CharField(max_length=250, blank=False, null=False, default='')
    imagen = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    imagen_thumb = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'lineas'


class PuntosAlmacenes(models.Model):
    punto_almacen_id = models.AutoField(primary_key=True, db_column='punto_almacen_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    almacen_id = models.ForeignKey(Almacenes, to_field='almacen_id', on_delete=models.PROTECT, db_column='almacen_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'puntos_almacenes'
