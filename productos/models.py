from django.db import models
from status.models import Status
from utils.custome_db_types import DateTimeFieldCustome
from configuraciones.models import Lineas
from permisos.models import UsersPerfiles


class Productos(models.Model):
    producto_id = models.AutoField(primary_key=True, db_column='producto_id')
    linea_id = models.ForeignKey(Lineas, to_field='linea_id', on_delete=models.PROTECT, db_column='linea_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    producto = models.CharField(max_length=250, unique=True, blank=False, null=False)
    codigo = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.CharField(max_length=250, blank=False, null=False)
    stock_minimo = models.IntegerField(blank=False, null=False, default=0)

    precio = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    precio_factura = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo_rotura = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'productos'


class ProductosImagenes(models.Model):
    producto_imagen_id = models.AutoField(primary_key=True, db_column='producto_imagen_id')
    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')
    imagen = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    imagen_thumb = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    posicion = models.IntegerField(null=False, blank=False, default=1)

    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'productos_imagenes'


class ProductosRelacionados(models.Model):
    producto_relacionado_id = models.AutoField(primary_key=True, db_column='producto_relacionado_id')
    producto_id = models.ForeignKey(Productos, verbose_name='prod1r', related_name='primer_prodr', on_delete=models.PROTECT, db_column='producto_id', to_field='producto_id')
    producto_relacion_id = models.ForeignKey(Productos, verbose_name='prod2r', related_name='segundo_prodr', on_delete=models.PROTECT, db_column='producto_relacion_id', to_field='producto_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'productos_relacionados'
