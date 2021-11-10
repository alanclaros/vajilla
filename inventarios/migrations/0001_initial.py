# Generated by Django 3.2.8 on 2021-10-12 14:35

from django.db import migrations, models
import django.db.models.deletion
import utils.custome_db_types


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0002_productos_init_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registros',
            fields=[
                ('registro_id', models.AutoField(db_column='registro_id', primary_key=True, serialize=False)),
                ('almacen2_id', models.IntegerField(default=0)),
                ('tipo_movimiento', models.CharField(max_length=50)),
                ('numero_registro', models.IntegerField(default=0)),
                ('fecha', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('porcentaje_descuento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('concepto', models.CharField(max_length=250)),
                ('user_perfil_id_anula', models.IntegerField(blank=True, null=True)),
                ('motivo_anula', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('almacen_id', models.ForeignKey(db_column='almacen_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.almacenes')),
                ('punto_id', models.ForeignKey(db_column='punto_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.puntos')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
                ('user_perfil_id', models.ForeignKey(db_column='user_perfil_id', on_delete=django.db.models.deletion.PROTECT, to='permisos.usersperfiles')),
            ],
            options={
                'db_table': 'registros',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('stock_id', models.AutoField(db_column='stock_id', primary_key=True, serialize=False)),
                ('cantidad', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('user_perfil_id_anula', models.IntegerField(blank=True, null=True)),
                ('motivo_anula', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('almacen_id', models.ForeignKey(db_column='almacen_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.almacenes')),
                ('producto_id', models.ForeignKey(db_column='producto_id', on_delete=django.db.models.deletion.PROTECT, to='productos.productos')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
                ('user_perfil_id', models.ForeignKey(db_column='user_perfil_id', on_delete=django.db.models.deletion.PROTECT, to='permisos.usersperfiles')),
            ],
            options={
                'db_table': 'stock',
            },
        ),
        migrations.CreateModel(
            name='RegistrosDetalles',
            fields=[
                ('registro_detalle_id', models.AutoField(db_column='registro_detalle_id', primary_key=True, serialize=False)),
                ('cantidad', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('costo', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('porcentaje_descuento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('producto_id', models.ForeignKey(db_column='producto_id', on_delete=django.db.models.deletion.PROTECT, to='productos.productos')),
                ('punto_id', models.ForeignKey(db_column='punto_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.puntos')),
                ('registro_id', models.ForeignKey(db_column='registro_id', on_delete=django.db.models.deletion.PROTECT, to='inventarios.registros')),
            ],
            options={
                'db_table': 'registros_detalles',
            },
        ),
    ]
