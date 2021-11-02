# Generated by Django 3.2.8 on 2021-10-10 15:51

from django.db import migrations, models
import django.db.models.deletion
import utils.custome_db_types


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('permisos', '0002_permisos_init_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Almacenes',
            fields=[
                ('almacen_id', models.AutoField(db_column='almacen_id', primary_key=True, serialize=False)),
                ('almacen', models.CharField(default='', max_length=150)),
                ('codigo', models.CharField(default='', max_length=20)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
            ],
            options={
                'db_table': 'almacenes',
            },
        ),
        migrations.CreateModel(
            name='Ciudades',
            fields=[
                ('ciudad_id', models.AutoField(db_column='ciudad_id', primary_key=True, serialize=False)),
                ('ciudad', models.CharField(max_length=150)),
                ('codigo', models.CharField(max_length=50)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
            ],
            options={
                'db_table': 'ciudades',
            },
        ),
        migrations.CreateModel(
            name='Configuraciones',
            fields=[
                ('configuracion_id', models.IntegerField(primary_key=True, serialize=False)),
                ('cant_per_page', models.IntegerField()),
                ('usar_fecha_servidor', models.CharField(default='si', max_length=20)),
                ('fecha_sistema', utils.custome_db_types.DateFieldCustome(blank=True, null=True)),
            ],
            options={
                'db_table': 'configuraciones',
            },
        ),
        migrations.CreateModel(
            name='Paises',
            fields=[
                ('pais_id', models.IntegerField(db_column='pais_id', primary_key=True, serialize=False)),
                ('pais', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'paises',
            },
        ),
        migrations.CreateModel(
            name='Puntos',
            fields=[
                ('punto_id', models.AutoField(db_column='punto_id', primary_key=True, serialize=False)),
                ('punto', models.CharField(max_length=150)),
                ('codigo', models.CharField(max_length=50)),
                ('impresora_reportes', models.CharField(max_length=250)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
            ],
            options={
                'db_table': 'puntos',
            },
        ),
        migrations.CreateModel(
            name='TiposMonedas',
            fields=[
                ('tipo_moneda_id', models.IntegerField(db_column='tipo_moneda_id', primary_key=True, serialize=False)),
                ('tipo_moneda', models.CharField(max_length=150)),
                ('codigo', models.CharField(max_length=50)),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
            ],
            options={
                'db_table': 'tipos_monedas',
            },
        ),
        migrations.CreateModel(
            name='Sucursales',
            fields=[
                ('sucursal_id', models.AutoField(db_column='sucursal_id', primary_key=True, serialize=False)),
                ('sucursal', models.CharField(max_length=250)),
                ('codigo', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=250)),
                ('empresa', models.CharField(max_length=250)),
                ('direccion', models.CharField(max_length=250)),
                ('ciudad', models.CharField(max_length=250)),
                ('telefonos', models.CharField(max_length=250)),
                ('actividad', models.CharField(max_length=250)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('ciudad_id', models.ForeignKey(db_column='ciudad_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.ciudades')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
                ('user_perfil_id', models.ForeignKey(db_column='user_perfil_id', on_delete=django.db.models.deletion.PROTECT, to='permisos.usersperfiles')),
            ],
            options={
                'db_table': 'sucursales',
            },
        ),
        migrations.CreateModel(
            name='PuntosAlmacenes',
            fields=[
                ('punto_almacen_id', models.AutoField(db_column='punto_almacen_id', primary_key=True, serialize=False)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('almacen_id', models.ForeignKey(db_column='almacen_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.almacenes')),
                ('punto_id', models.ForeignKey(db_column='punto_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.puntos')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
            ],
            options={
                'db_table': 'puntos_almacenes',
            },
        ),
        migrations.AddField(
            model_name='puntos',
            name='sucursal_id',
            field=models.ForeignKey(db_column='sucursal_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.sucursales'),
        ),
        migrations.AddField(
            model_name='puntos',
            name='user_perfil_id',
            field=models.ForeignKey(db_column='user_perfil_id', on_delete=django.db.models.deletion.PROTECT, to='permisos.usersperfiles'),
        ),
        migrations.CreateModel(
            name='Monedas',
            fields=[
                ('moneda_id', models.IntegerField(db_column='moneda_id', primary_key=True, serialize=False)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
                ('tipo_moneda_id', models.ForeignKey(db_column='tipo_moneda_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.tiposmonedas')),
            ],
            options={
                'db_table': 'monedas',
            },
        ),
        migrations.CreateModel(
            name='Lineas',
            fields=[
                ('linea_id', models.AutoField(db_column='linea_id', primary_key=True, serialize=False)),
                ('linea', models.CharField(default='', max_length=150)),
                ('codigo', models.CharField(default='', max_length=150)),
                ('linea_principal', models.IntegerField(default=0)),
                ('linea_superior_id', models.IntegerField(default=0)),
                ('descripcion', models.CharField(default='', max_length=250)),
                ('imagen', models.CharField(default='', max_length=250, unique=True)),
                ('imagen_thumb', models.CharField(default='', max_length=250, unique=True)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
            ],
            options={
                'db_table': 'lineas',
            },
        ),
        migrations.AddField(
            model_name='ciudades',
            name='pais_id',
            field=models.ForeignKey(db_column='pais_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.paises'),
        ),
        migrations.AddField(
            model_name='ciudades',
            name='status_id',
            field=models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status'),
        ),
        migrations.AddField(
            model_name='ciudades',
            name='user_perfil_id',
            field=models.ForeignKey(db_column='user_perfil_id', on_delete=django.db.models.deletion.PROTECT, to='permisos.usersperfiles'),
        ),
        migrations.CreateModel(
            name='Cajas',
            fields=[
                ('caja_id', models.AutoField(db_column='caja_id', primary_key=True, serialize=False)),
                ('caja', models.CharField(max_length=150)),
                ('codigo', models.CharField(max_length=50)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('punto_id', models.ForeignKey(db_column='punto_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.puntos')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
                ('tipo_moneda_id', models.ForeignKey(db_column='tipo_moneda_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.tiposmonedas')),
                ('user_perfil_id', models.ForeignKey(db_column='user_perfil_id', on_delete=django.db.models.deletion.PROTECT, to='permisos.usersperfiles')),
            ],
            options={
                'db_table': 'cajas',
            },
        ),
    ]
