from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm

# imagen
from reportlab.platypus import Image, Table, TableStyle
from reportlab.lib import colors
from django.apps import apps

# cabecera
from reportes.cabecera import cabecera

# modelos
from configuraciones.models import Cajas
from cajas.models import CajasEgresos
from django.contrib.auth.models import User

# settings
from django.conf import settings

# utils
from utils.dates_functions import get_date_show
from utils.permissions import get_sucursal_settings, current_date, report_date

# clases
from controllers.cajas.CajasEgresosController import CajasEgresosController

import os


def rptCajaEgresoRecibo(buffer, caja_egreso_id):
    # pdf
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # controller
    ce_controller = CajasEgresosController()
    # datos del ingreso
    ce_data = CajasEgresos.objects.select_related('user_perfil_id').get(pk=caja_egreso_id)
    caja_reporte = Cajas.objects.select_related('punto_id').select_related('punto_id__sucursal_id').select_related('punto_id__sucursal_id__ciudad_id').select_related('tipo_moneda_id').get(pk=ce_data.caja_id.caja_id)

    # fecha operacion
    fecha_operacion = get_date_show(fecha=ce_data.fecha, formato='dd-MMM-yyyy HH:ii')
    usuario_operacion = ce_data.user_perfil_id.user_id.username
    monto = ce_data.monto
    concepto = ce_data.concepto

    # anulado
    anulado = ''
    user_anula = ''
    motivo_anula = ''
    if ce_data.status_id.status_id == ce_controller.anulado:
        anulado = 'si'
        user_perfil_del = apps.get_model('permisos', 'UsersPerfiles').objects.get(pk=ce_data.user_perfil_id_anula)
        user_del = User.objects.get(pk=user_perfil_del.user_id.id)
        user_anula = user_del.username
        motivo_anula = ce_data.motivo_anula

    # datos reporte
    datos_reporte = get_sucursal_settings(caja_reporte.punto_id.sucursal_id.sucursal_id)
    datos_reporte['titulo'] = 'Egreso de Caja: ' + caja_reporte.punto_id.punto + '-' + caja_reporte.codigo
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
    texto.setFont("Helvetica", 10)
    texto.setFillColorRGB(0, 0, 0)

    # dibujamos
    # usuario operacion
    pdf.setFont('Helvetica', 10)
    pdf.drawRightString(posX*mm, posY*mm, 'Usuario: ')
    texto.textOut(usuario_operacion)

    # fecha
    pdf.drawRightString(70*mm, posY*mm, 'Fecha: ')
    texto.moveCursor(40*mm, 0)
    texto.textOut(fecha_operacion)

    # monto
    pdf.drawRightString(130*mm, posY*mm, 'Monto: ')
    texto.moveCursor(60*mm, 0)
    texto.textOut(str(monto) + ' ' + caja_reporte.tipo_moneda_id.codigo + ' (' + str(caja_egreso_id) + ')')

    # si es que esta anulado
    if anulado == 'si':
        pdf.setFont('Helvetica-Bold', 10)
        pdf.drawRightString(180*mm, posY*mm, 'ANULADO: ')
        texto.moveCursor(50*mm, 0)
        texto.textOut(user_anula)
        pdf.setFont('Helvetica', 10)

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
    pdf.setTitle("Ingreso a Caja")
    pdf.setSubject("ingreso a Caja, " + settings.NOMBRE_SISTEMA)
    pdf.save()
