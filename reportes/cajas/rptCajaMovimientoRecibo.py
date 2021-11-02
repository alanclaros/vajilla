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
from cajas.models import CajasMovimientos
from django.contrib.auth.models import User

# settings
from django.conf import settings

# utils
from utils.permissions import get_sucursal_settings, current_date, report_date
from utils.dates_functions import get_date_show

# clases
from controllers.cajas.CajasMovimientosController import CajasMovimientosController

import os


def rptCajaMovimientoRecibo(buffer, caja_movimiento_id):
    # pdf
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # controller
    caja_movimiento_controller = CajasMovimientosController()
    # datos del movimiento
    caja_movimiento_dato = CajasMovimientos.objects.select_related('caja1_id').select_related('caja2_id').select_related(
        'caja1_user_perfil_id').select_related('caja2_user_perfil_id').select_related('tipo_moneda_id').get(pk=caja_movimiento_id)
    caja_reporte = Cajas.objects.select_related('punto_id').select_related('punto_id__sucursal_id').select_related(
        'punto_id__sucursal_id__ciudad_id').select_related('tipo_moneda_id').get(pk=caja_movimiento_dato.caja1_id.caja_id)

    # fecha operacion
    fecha_operacion = get_date_show(fecha=caja_movimiento_dato.fecha, formato='dd-MMM-yyyy HH:ii')
    usuario_envia = caja_movimiento_dato.caja1_user_perfil_id.user_id.username
    usuario_recibe = caja_movimiento_dato.caja2_user_perfil_id.user_id.username
    monto = caja_movimiento_dato.monto
    concepto = caja_movimiento_dato.concepto

    # anulado
    anulado = ''
    user_anula = ''
    motivo_anula = ''
    if caja_movimiento_dato.status_id.status_id == caja_movimiento_controller.anulado:
        anulado = 'si'
        user_del = User.objects.get(pk=caja_movimiento_dato.user_perfil_id_anula)
        user_perfil_anula = apps.get_model('permisos', 'UsersPerfiles').objects.get(pk=caja_movimiento_dato.user_perfil_id_anula)
        user_anula = user_perfil_anula.user_id.username
        motivo_anula = caja_movimiento_dato.motivo_anula

    # datos reporte
    datos_reporte = get_sucursal_settings(caja_reporte.punto_id.sucursal_id.sucursal_id)
    datos_reporte['titulo'] = 'Movimiento de Caja: ' + caja_movimiento_dato.caja1_id.punto_id.punto + ' ' + caja_movimiento_dato.caja1_id.codigo
    datos_reporte['fecha_impresion'] = report_date()
    dir_img = os.path.join(settings.STATIC_ROOT, 'img/logo.png')
    datos_reporte['logo'] = dir_img

    cabecera(pdf, **datos_reporte)

    # datos del reporte
    posY = 240
    altoTxt = 6
    posX = 30

    # iniciando el objecto de texto en las coordenadas iniciales
    texto = pdf.beginText()
    texto.setTextOrigin(posX*mm, posY*mm)
    pdf.setFont('Helvetica', 10)
    texto.setFont("Helvetica", 10)
    texto.setFillColorRGB(0, 0, 0)

    # dibujamos
    # cajas
    pdf.drawRightString(posX*mm, posY*mm, 'Movimiento: ')
    movimiento_cajas = caja_movimiento_dato.caja1_id.punto_id.punto + ' - ' + caja_movimiento_dato.caja1_id.codigo + \
        '   envia a   ' + caja_movimiento_dato.caja2_id.punto_id.punto + ' - ' + caja_movimiento_dato.caja2_id.codigo
    texto.textOut(movimiento_cajas)

    # usuario envia
    posY = posY-altoTxt
    texto.setTextOrigin(posX*mm, posY*mm)
    pdf.drawRightString(posX*mm, posY*mm, 'Envia: ')
    texto.textOut(usuario_envia)

    # fecha
    pdf.drawRightString(70*mm, posY*mm, 'Fecha: ')
    texto.moveCursor(40*mm, 0)
    texto.textOut(fecha_operacion)

    # monto
    pdf.drawRightString(130*mm, posY*mm, 'Monto: ')
    texto.moveCursor(60*mm, 0)
    texto.textOut(str(monto) + ' ' + caja_reporte.tipo_moneda_id.codigo + ' (' + str(caja_movimiento_id) + ')')

    # si es que esta anulado
    if anulado == 'si':
        pdf.setFont('Helvetica-Bold', 10)
        pdf.drawRightString(180*mm, posY*mm, 'ANULADO: ')
        texto.moveCursor(50*mm, 0)
        texto.textOut(user_anula)
        pdf.setFont('Helvetica', 10)

    # usuario recibe
    posY = posY-altoTxt
    pdf.drawRightString(posX*mm, posY*mm, 'Recibe: ')
    texto.setTextOrigin(posX*mm, posY*mm)
    if caja_movimiento_dato.status_id.status_id == caja_movimiento_controller.movimiento_caja_recibe:
        texto.textOut(usuario_recibe)
    else:
        texto.textOut('')

    # concepto
    posY = posY-altoTxt
    pdf.drawRightString(posX*mm, posY*mm, 'Concepto: ')
    texto.setTextOrigin(posX*mm, posY*mm)
    texto.textOut(concepto)

    # motivo anula
    if anulado == 'si':
        posY = posY-altoTxt
        pdf.drawRightString(posX*mm, posY*mm, 'Anula: ')
        texto.setTextOrigin(posX*mm, posY*mm)
        texto.textOut(motivo_anula)

    # dibujamos los objetos texto
    pdf.drawText(texto)

    # guardamos
    pdf.setAuthor("Alan Claros")
    pdf.setTitle("Movimiento de Caja")
    pdf.setSubject("movimiento de Caja, " + settings.NOMBRE_SISTEMA)
    pdf.save()
