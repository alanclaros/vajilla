# Generated by Django 3.2.8 on 2021-10-11 15:27

from django.db import migrations, models
import django.db.models.deletion
import utils.custome_db_types


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cajas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('producto_id', models.AutoField(db_column='producto_id', primary_key=True, serialize=False)),
                ('producto', models.CharField(max_length=250, unique=True)),
                ('codigo', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=250)),
                ('stock_minimo', models.IntegerField(default=0)),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('precio_factura', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('costo_rotura', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('linea_id', models.ForeignKey(db_column='linea_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.lineas')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
                ('user_perfil_id', models.ForeignKey(db_column='user_perfil_id', on_delete=django.db.models.deletion.PROTECT, to='permisos.usersperfiles')),
            ],
            options={
                'db_table': 'productos',
            },
        ),
        migrations.CreateModel(
            name='ProductosRelacionados',
            fields=[
                ('producto_relacionado_id', models.AutoField(db_column='producto_relacionado_id', primary_key=True, serialize=False)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('producto_id', models.ForeignKey(db_column='producto_id', on_delete=django.db.models.deletion.PROTECT, related_name='primer_prodr', to='productos.productos', verbose_name='prod1r')),
                ('producto_relacion_id', models.ForeignKey(db_column='producto_relacion_id', on_delete=django.db.models.deletion.PROTECT, related_name='segundo_prodr', to='productos.productos', verbose_name='prod2r')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
            ],
            options={
                'db_table': 'productos_relacionados',
            },
        ),
        migrations.CreateModel(
            name='ProductosImagenes',
            fields=[
                ('producto_imagen_id', models.AutoField(db_column='producto_imagen_id', primary_key=True, serialize=False)),
                ('imagen', models.CharField(default='', max_length=250, unique=True)),
                ('imagen_thumb', models.CharField(default='', max_length=250, unique=True)),
                ('posicion', models.IntegerField(default=1)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('producto_id', models.ForeignKey(db_column='producto_id', on_delete=django.db.models.deletion.PROTECT, to='productos.productos')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
            ],
            options={
                'db_table': 'productos_imagenes',
            },
        ),
    ]
