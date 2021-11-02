from django.db import models

from status.models import Status
from utils.custome_db_types import DateTimeFieldCustome
from configuraciones.models import Puntos
from permisos.models import UsersPerfiles


class Clientes(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    nombres = models.CharField(max_length=150, blank=False, null=False)
    apellidos = models.CharField(max_length=150, blank=False, null=False)
    ci_nit = models.CharField(max_length=50, blank=False, null=False)
    telefonos = models.CharField(max_length=250, blank=False, null=False, default='')
    direccion = models.CharField(max_length=250, blank=False, null=False, default='')
    email = models.CharField(max_length=250, blank=False, null=False)
    razon_social = models.CharField(max_length=250, blank=False, null=False, default='')
    factura_a = models.CharField(max_length=250, blank=False, null=False, default='')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'clientes'
