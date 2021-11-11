# Generated by Django 3.2.8 on 2021-10-10 15:51

from django.db import migrations
from configuraciones.models import Configuraciones, Paises, Ciudades, Sucursales, Puntos, Cajas, TiposMonedas, Monedas, Almacenes, Lineas, PuntosAlmacenes
from permisos.models import UsersPerfiles
from status.models import Status


def load_data(apps, schema_editor):
    # configuraciones
    configuraciones_add = Configuraciones.objects.create(
        configuracion_id=1, cant_per_page=30,
        usar_fecha_servidor='si', fecha_sistema='now', minutos_antes_devolucion=180, minutos_despues_entrega=180,
        minutos_aviso_entregar=360, minutos_aviso_entregar_tarde=180,
        minutos_aviso_recoger=360, minutos_aviso_recoger_tarde=180,
        minutos_aviso_finalizar=180, minutos_aviso_finalizar_tarde=360)
    configuraciones_add.save()

    # paises
    paises_add = Paises.objects.create(pais_id=1, pais='Bolivia')
    paises_add.save()

    # datos
    user_perfil = UsersPerfiles.objects.get(pk=1)
    bolivia = Paises.objects.get(pk=1)
    status_activo = Status.objects.get(pk=1)

    # ciudades
    ciudad_add = Ciudades.objects.create(pais_id=bolivia, user_perfil_id=user_perfil, status_id=status_activo, ciudad='Cochabamba', codigo='CBA', created_at='now', updated_at='now')
    ciudad_add.save()

    # ciudad cbba
    cochabamba = Ciudades.objects.get(pk=1)

    # SUCURSALES
    sucursal_add = Sucursales.objects.create(ciudad_id=cochabamba, user_perfil_id=user_perfil, status_id=status_activo, sucursal='Sucursal Central', codigo='SC-CBA', email='acc.claros@gmail.com',
                                             empresa='El Copetin', direccion='Batallon Colorados 2357', ciudad='Cochabamba - Bolivia', telefonos='4400661 - 44006622 - 70300335 - 78333334 - 67402818', actividad='Eventos Sociales', created_at='now', updated_at='now')
    sucursal_add.save()
    # sucursal central
    sucursal_central = Sucursales.objects.get(pk=1)

    # puntos
    punto_add = Puntos.objects.create(sucursal_id=sucursal_central, user_perfil_id=user_perfil, status_id=status_activo, punto='Punto 1',
                                      codigo='P1', impresora_reportes='impresora reportes', created_at='now', updated_at='now')
    punto_add.save()
    punto1 = Puntos.objects.get(pk=1)

    # almacen
    almacen_add = Almacenes.objects.create(sucursal_id=sucursal_central, status_id=status_activo, almacen='Almacen 01 Central',
                                           codigo='AL01', created_at='now', updated_at='now')
    almacen_add.save()
    almacen_central = Almacenes.objects.get(pk=1)

    # puntos almacenes
    puntos_almacenes_add = PuntosAlmacenes.objects.create(punto_id=punto1, almacen_id=almacen_central, status_id=status_activo, created_at='now', updated_at='now')
    puntos_almacenes_add.save()

    # lineas
    # linea = Lineas.objects.create(linea='Vajilla', codigo='vajilla', linea_principal=1, linea_superior_id=0, descripcion='', imagen='vajilla.jpg',
    #                               imagen_thumb='vajilla_thumb.jpg', status_id=status_activo, created_at='now', updated_at='now')
    # linea.save()
    # linea = Lineas.objects.create(linea='Manteleria', codigo='manteleria', linea_principal=1, linea_superior_id=0, descripcion='', imagen='manteleria.jpg',
    #                               imagen_thumb='manteleria_thumb.jpg', status_id=status_activo, created_at='now', updated_at='now')
    # linea.save()
    # linea = Lineas.objects.create(linea='SobreManteles', codigo='sobremanteles', linea_principal=1, linea_superior_id=0, descripcion='', imagen='sobremanteles.jpg',
    #                               imagen_thumb='sobremanteles_thumb.jpg', status_id=status_activo, created_at='now', updated_at='now')
    # linea.save()
    # linea = Lineas.objects.create(linea='Caminitos', codigo='caminitos', linea_principal=1, linea_superior_id=0, descripcion='', imagen='caminitos.jpg',
    #                               imagen_thumb='caminitos_thumb.jpg', status_id=status_activo, created_at='now', updated_at='now')
    # linea.save()
    # linea = Lineas.objects.create(linea='Servilletas', codigo='servilletas', linea_principal=1, linea_superior_id=0, descripcion='', imagen='servilletas.jpg',
    #                               imagen_thumb='servilletas_thumb.jpg', status_id=status_activo, created_at='now', updated_at='now')
    # linea.save()
    # linea = Lineas.objects.create(linea='Moñas', codigo='monias', linea_principal=1, linea_superior_id=0, descripcion='', imagen='monias.jpg',
    #                               imagen_thumb='monias_thumb.jpg', status_id=status_activo, created_at='now', updated_at='now')
    # linea.save()
    # linea = Lineas.objects.create(linea='Cabezal', codigo='cabecal', linea_principal=1, linea_superior_id=0, descripcion='', imagen='cabecal.jpg',
    #                               imagen_thumb='cabecal_thumb.jpg', status_id=status_activo, created_at='now', updated_at='now')
    # linea.save()
    # linea = Lineas.objects.create(linea='Cobertores', codigo='cobertores', linea_principal=1, linea_superior_id=0, descripcion='', imagen='cobertores.jpg',
    #                               imagen_thumb='cobertores_thumb.jpg', status_id=status_activo, created_at='now', updated_at='now')
    # linea.save()
    # linea = Lineas.objects.create(linea='Faldones', codigo='faldones', linea_principal=1, linea_superior_id=0, descripcion='', imagen='faldones.jpg',
    #                               imagen_thumb='faldones_thumb.jpg', status_id=status_activo, created_at='now', updated_at='now')
    # linea.save()
    # linea = Lineas.objects.create(linea='CanCan', codigo='cancan', linea_principal=1, linea_superior_id=0, descripcion='', imagen='cancan.jpg',
    #                               imagen_thumb='cancan_thumb.jpg', status_id=status_activo, created_at='now', updated_at='now')
    # linea.save()
    # linea = Lineas.objects.create(linea='Muletones', codigo='muletones', linea_principal=1, linea_superior_id=0, descripcion='', imagen='muletones.jpg',
    #                               imagen_thumb='muletones_thumb.jpg', status_id=status_activo, created_at='now', updated_at='now')
    # linea.save()
    # linea = Lineas.objects.create(linea='Mesas', codigo='mesas', linea_principal=1, linea_superior_id=0, descripcion='', imagen='mesas.jpg',
    #                               imagen_thumb='mesas_thumb.jpg', status_id=status_activo, created_at='now', updated_at='now')
    # linea.save()
    # linea = Lineas.objects.create(linea='Toldos', codigo='toldos', linea_principal=1, linea_superior_id=0, descripcion='', imagen='toldos.jpg',
    #                               imagen_thumb='toldos_thumb.jpg', status_id=status_activo, created_at='now', updated_at='now')
    # linea.save()
    # linea = Lineas.objects.create(linea='Laterales', codigo='laterales', linea_principal=1, linea_superior_id=0, descripcion='', imagen='laterales.jpg',
    #                               imagen_thumb='laterales_thumb.jpg', status_id=status_activo, created_at='now', updated_at='now')
    # linea.save()
    # linea = Lineas.objects.create(linea='Alfombras', codigo='alfombras', linea_principal=1, linea_superior_id=0, descripcion='', imagen='alfombras.jpg',
    #                               imagen_thumb='alfombras_thumb.jpg', status_id=status_activo, created_at='now', updated_at='now')
    # linea.save()

    # tipos monedas
    tipo_moneda_add = TiposMonedas.objects.create(tipo_moneda_id=1, status_id=status_activo, tipo_moneda='Bolivianos', codigo='Bs.')
    tipo_moneda_add.save()

    # monedas
    tipo_bs = TiposMonedas.objects.get(pk=1)
    # bs
    moneda = Monedas.objects.create(moneda_id=1, tipo_moneda_id=tipo_bs, monto=0.10, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=2, tipo_moneda_id=tipo_bs, monto=0.20, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=3, tipo_moneda_id=tipo_bs, monto=0.50, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=4, tipo_moneda_id=tipo_bs, monto=1.00, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=5, tipo_moneda_id=tipo_bs, monto=2.00, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=6, tipo_moneda_id=tipo_bs, monto=5.00, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=7, tipo_moneda_id=tipo_bs, monto=10.00, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=8, tipo_moneda_id=tipo_bs, monto=20.00, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=9, tipo_moneda_id=tipo_bs, monto=50.00, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=10, tipo_moneda_id=tipo_bs, monto=100.00, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=11, tipo_moneda_id=tipo_bs, monto=200.00, status_id=status_activo)
    moneda.save()

    # cajas
    caja_Bs = Cajas.objects.create(punto_id=punto1, tipo_moneda_id=tipo_bs, user_perfil_id=user_perfil, status_id=status_activo, caja=' P1-Caja1', codigo='P1-C1', created_at='now', updated_at='now')
    caja_Bs.save()


def delete_data(apps, schema_editor):
    lineas_del = apps.get_model('configuraciones', 'Lineas')
    lineas_del.objects.all().delete

    puntos_almacenes_del = apps.get_model('configuraciones', 'PuntosAlmacenes')
    puntos_almacenes_del.objects.all().delete

    almacenes_del = apps.get_model('configuraciones', 'Almacenes')
    almacenes_del.objects.all().delete

    cajas_del = apps.get_model('configuraciones', 'Cajas')
    cajas_del.objects.all().delete

    monedas_del = apps.get_model('configuraciones', 'Monedas')
    monedas_del.objects.all().delete

    tipos_monedas_del = apps.get_model('configuraciones', 'TiposMonedas')
    tipos_monedas_del.objects.all().delete

    puntos_del = apps.get_model('configuraciones', 'Puntos')
    puntos_del.objects.all().delete

    sucursales_del = apps.get_model('configuraciones', 'Sucursales')
    sucursales_del.objects.all().delete

    ciudades_del = apps.get_model('configuraciones', 'Ciudades')
    ciudades_del.objects.all().delete

    paises_del = apps.get_model('configuraciones', 'Paises')
    paises_del.objects.all().delete

    configuraciones_del = apps.get_model('configuraciones', 'Configuraciones')
    configuraciones_del.objects.all().delete


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data, delete_data),
    ]
