from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
from django.apps import apps

# imagen
from reportlab.platypus import Image, Table, TableStyle
from reportlab.lib import colors

# cabecera
from reportes.cabecera import cabecera

# modelos
from configuraciones.models import Cajas, Puntos, Sucursales, TiposMonedas, Monedas
from cajas.models import CajasOperaciones, CajasOperacionesDetalles
from django.contrib.auth.models import User

# settings
from django.conf import settings

# utils
from utils.permissions import get_sucursal_settings, current_date, report_date
from utils.dates_functions import get_date_show

import os


def rptCajasIniciar(buffer, caja_id):
    # pdf
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # datos de caja
    caja_reporte = Cajas.objects.select_related('punto_id').select_related('tipo_moneda_id').get(pk=int(caja_id))
    caja_operacion = CajasOperaciones.objects.filter(caja_id=caja_reporte, fecha=current_date())[:1].get()
    filtros = {}
    filtros['caja_operacion_id'] = caja_operacion
    filtros['moneda_id__status_id_id'] = settings.STATUS_ACTIVO
    caja_operacion_detalle = CajasOperacionesDetalles.objects.select_related('moneda_id').filter(**filtros).order_by('moneda_id__monto')

    # fecha operacion
    fecha_operacion = get_date_show(fecha=caja_operacion.fecha, formato='dd-MMM-yyyy')
    usuario_inicia = ''
    usuario_inicia_recibe = ''
    monto = caja_operacion.monto_apertura

    # usuario apertura y apertura_recibe
    if caja_operacion.usuario_perfil_apertura_id > 0:
        usuario_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(pk=caja_operacion.usuario_perfil_apertura_id)
        usuario_r = User.objects.get(pk=usuario_perfil.user_id.id)
        usuario_inicia = usuario_r.username

    if caja_operacion.usuario_perfil_apertura_r_id > 0:
        usuario_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(pk=caja_operacion.usuario_perfil_apertura_r_id)
        usuario_r = User.objects.get(pk=usuario_perfil.user_id.id)
        usuario_inicia_recibe = usuario_r.username

    # datos reporte
    # print('sucursal..', CajaReporte.punto_id.sucursal_id_id)
    datos_reporte = get_sucursal_settings(caja_reporte.punto_id.sucursal_id_id)
    datos_reporte['titulo'] = 'Inicio de Caja: ' + caja_reporte.punto_id.punto + '-' + caja_reporte.codigo
    datos_reporte['fecha_impresion'] = report_date()
    dir_img = os.path.join(settings.STATIC_ROOT, 'img/logo.png')
    datos_reporte['logo'] = dir_img

    cabecera(pdf, **datos_reporte)

    # datos del reporte
    posY = 240
    altoTxt = 6
    posX = 60

    # iniciando el objecto de texto en las coordenadas iniciales
    texto = pdf.beginText()
    texto.setTextOrigin(posX*mm, posY*mm)
    texto.setFont("Helvetica", 10)
    texto.setFillColorRGB(0, 0, 0)

    # dibujamos
    # usuario apertura
    pdf.setFont('Helvetica', 10)
    pdf.drawRightString(posX*mm, posY*mm, 'Usuario Apertura: ')
    texto.textOut(usuario_inicia)

    # usuario recibe
    pdf.drawRightString(140*mm, posY*mm, 'Usuario Recibe: ')
    texto.moveCursor(80*mm, 0)
    texto.textOut(usuario_inicia_recibe)

    # fecha
    posY = posY-altoTxt
    pdf.drawRightString(posX*mm, posY*mm, 'Fecha: ')
    texto.setTextOrigin(posX*mm, posY*mm)
    texto.textOut(fecha_operacion)

    # monto
    pdf.drawRightString(140*mm, posY*mm, 'Monto: ')
    texto.moveCursor(80*mm, 0)
    texto.textOut(str(monto) + ' ' + caja_reporte.tipo_moneda_id.codigo)

    # dibujamos los objetos texto
    pdf.drawText(texto)

    # tabla
    data = []
    data.append(['Corte', 'cantidad', 'Total'])
    filas = 0

    for detalle in caja_operacion_detalle:
        datos = []
        datos.append(str(detalle.moneda_id.monto) + ' ' + caja_reporte.tipo_moneda_id.codigo)
        datos.append(str(detalle.cantidad_apertura))
        datos.append(str(detalle.cantidad_apertura * detalle.moneda_id.monto))

        data.append(datos)
        filas += 1

    t = Table(data, colWidths=[40*mm, 40*mm, 40*mm])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (2, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                           ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black),
                           ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))

    width = 20*mm
    height = 20*mm
    alto_celda = 6.4  # hicimos la primera tabla para $us, con 6 filas
    x = 45*mm
    y = (185 - ((filas-6)*alto_celda))*mm

    # f = Table(data)
    t.wrapOn(pdf, width, height)
    t.drawOn(pdf, x, y)

    # guardamos
    pdf.setAuthor("Alan Claros")
    pdf.setTitle("Inicio de Caja")
    pdf.setSubject("Inicio de Caja, " + settings.NOMBRE_SISTEMA)
    pdf.save()
