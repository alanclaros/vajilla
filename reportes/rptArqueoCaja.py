from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import pagesizes
#from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm

from datetime import datetime

# imagen
from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle
from reportlab.platypus import SimpleDocTemplate  # BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# cabecera
from reportes.cabecera import cabecera

# modelos
from configuraciones.models import Cajas, Puntos, Sucursales, TiposMonedas, Monedas

# settings
from django.conf import settings

# utils
from utils.permissions import get_sucursal_settings, report_date
from utils.dates_functions import get_date_system, get_date_show

# clases
from controllers.reportes.ReportesController import ReportesController

import os


# tamanio de pagina
pagesize = pagesizes.portrait(pagesizes.letter)
RPT_SUCURSAL_ID = 0
NOMBRE_CAJA = ''


def myFirstPage(canvas, doc):
    canvas.saveState()

    # canvas.setFont('Times-Bold', 16)
    # canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
    # canvas.setFont('Times-Roman', 9)
    # canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)

    datosReporte = get_sucursal_settings(RPT_SUCURSAL_ID)
    datosReporte['titulo'] = 'Arqueo de Caja: ' + NOMBRE_CAJA
    datosReporte['fecha_impresion'] = report_date()
    dir_img = os.path.join(settings.STATIC_ROOT, 'img/logo.png')
    datosReporte['logo'] = dir_img

    cabecera(canvas, **datosReporte)

    # canvas.setFont('Helvetica', 8)
    # canvas.drawString(15 * mm, 10 * mm, "footer todas las hojas %d" % (doc.page,))
    # canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "Created: %s" % datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    canvas.setFont('Times-Italic', 8)
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))

    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()

    canvas.setFont('Times-Italic', 8)
    #canvas.drawString(15 * mm, 10 * mm, "footer todas las hojas %d" % (doc.page,))
    #canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "Created: %s" % datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))
    canvas.restoreState()


def rptArqueoCaja(buffer_pdf, caja_id, fecha):
    # pdf
    #pdf = canvas.Canvas(buffer, pagesize=letter)

    # datos de la caja
    caja_actual = Cajas.objects.select_related('punto_id').select_related('punto_id__sucursal_id').get(pk=caja_id)
    global RPT_SUCURSAL_ID
    RPT_SUCURSAL_ID = caja_actual.punto_id.sucursal_id.sucursal_id
    global NOMBRE_CAJA
    NOMBRE_CAJA = caja_actual.punto_id.punto + '-' + caja_actual.caja

    doc = SimpleDocTemplate(buffer_pdf, pagesize=letter, leftMargin=10 * mm, rightMargin=10 * mm, topMargin=10 * mm, bottomMargin=15 * mm)

    """datos del reporte"""
    reporte_controller = ReportesController()
    datos_reporte = reporte_controller.datos_arqueo_caja(caja_id=caja_id, fecha=fecha)

    # tabla
    data = []
    data.append(['Fecha', 'Concepto', 'Monto'])
    filas = 0
    total = 0

    for dato in datos_reporte:
        total += dato['monto']
        datos = []
        datos.append(str(dato['fecha']))

        # concepto = str(dato['concepto'])
        # if len(concepto) > 75:
        #     concepto = concepto[0:75] + '..'
        concepto = Paragraph(str(dato['concepto']))

        datos.append(concepto)

        datos.append(str(dato['monto']) + ' ' + caja_actual.tipo_moneda_id.codigo)

        data.append(datos)
        filas += 1

    # aniadimos el total
    datos = []
    datos.append('')
    datos.append('Total: ')
    datos.append(str(total) + ' ' + caja_actual.tipo_moneda_id.codigo)

    data.append(datos)

    tabla_datos = Table(data, colWidths=[35*mm, 120*mm, 25*mm], repeatRows=1)
    tabla_datos.setStyle(TableStyle([('BACKGROUND', (0, 0), (2, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                     #('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                                     ('ALIGN', (2, 0), (2, filas+1), 'RIGHT'),
                                     ('ALIGN', (1, filas+1), (1, filas+1), 'RIGHT'),
                                     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                     ('FONTSIZE', (0, 0), (2, 0), 10),
                                     ('FONTSIZE', (0, 1), (-1, -1), 9),
                                     ('FONTNAME', (0, 0), (2, 0), 'Helvetica'),
                                     ('FONTNAME', (0, 1), (2, filas), 'Helvetica'),
                                     ('FONTNAME', (0, filas+1), (2, filas+1), 'Helvetica-Bold'),
                                     ('LEFTPADDING', (0, 0), (-1, -1), 2),
                                     ('RIGHTPADDING', (0, 1), (-1, -1), 1),
                                     ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))

    #table = Table(tdata, colWidths=colwidths, repeatRows=2)
    # table.setStyle(TableStyle(tstyledata))

    Story = []
    Story.append(Spacer(100*mm, 22*mm))
    Story.append(tabla_datos)

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
