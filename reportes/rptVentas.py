from reportlab.lib.pagesizes import letter
from reportlab.lib import pagesizes
from reportlab.lib.units import mm

# imagen
from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# cabecera
from reportes.cabecera import cabecera

# modelos
from configuraciones.models import Puntos
from permisos.models import UsersPerfiles

# settings
from django.conf import settings

# utils
from utils.permissions import get_sucursal_settings, report_date

# clases
from controllers.reportes.ReportesController import ReportesController


import os
import copy

# tamanio de pagina
pagesize = pagesizes.portrait(pagesizes.letter)
RPT_SUCURSAL_ID = 0
DATO_CAJA = ''


def myFirstPage(canvas, doc):
    canvas.saveState()

    datosReporte = get_sucursal_settings(RPT_SUCURSAL_ID)
    datosReporte['titulo'] = 'Ventas ' + DATO_CAJA
    datosReporte['fecha_impresion'] = report_date()
    dir_img = os.path.join(settings.STATIC_ROOT, 'img/logo.png')
    datosReporte['logo'] = dir_img

    cabecera(canvas, **datosReporte)

    canvas.setFont('Times-Italic', 8)
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))

    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()

    canvas.setFont('Times-Italic', 8)
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))
    canvas.restoreState()


def rptVentas(buffer_pdf, usuario, ciudad_id, sucursal_id, punto_id, fecha_ini, fecha_fin, anulados, preventa, venta, salida, vuelta, finalizado):

    # datos sucursal
    user_perfil = UsersPerfiles.objects.get(user_id=usuario)
    punto = Puntos.objects.get(pk=user_perfil.punto_id)
    sucursal_id_user = punto.sucursal_id.sucursal_id
    global RPT_SUCURSAL_ID
    RPT_SUCURSAL_ID = sucursal_id_user

    global DATO_CAJA
    if anulados == 'si':
        DATO_CAJA = 'Anulados'
    else:
        DATO_CAJA = ''

    styles = getSampleStyleSheet()
    # personalizamos
    style_ciudad = ParagraphStyle('ciudad',
                                  fontName="Helvetica-Bold",
                                  fontSize=12,
                                  parent=styles['Normal'],
                                  alignment=1,
                                  spaceAfter=10)

    style_sucursal = ParagraphStyle('sucursal',
                                    fontName="Helvetica-Bold",
                                    fontSize=10,
                                    parent=styles['Normal'],
                                    alignment=0,
                                    spaceAfter=2)

    style_punto = ParagraphStyle('punto',
                                 fontName="Helvetica-BoldOblique",
                                 fontSize=9,
                                 parent=styles['Normal'],
                                 alignment=0,
                                 spaceAfter=5)

    doc = SimpleDocTemplate(buffer_pdf, pagesize=letter, leftMargin=10 * mm, rightMargin=10 * mm, topMargin=10 * mm, bottomMargin=15 * mm)

    """datos del reporte"""
    reporte_controller = ReportesController()
    datos_reporte = reporte_controller.datos_ventas(usuario, ciudad_id, sucursal_id, punto_id, fecha_ini, fecha_fin, anulados, preventa, venta, salida, vuelta, finalizado)
    # print(datos_reporte)

    Story = []
    Story.append(Spacer(100*mm, 22*mm))
    fecha_reporte = 'Del: ' + fecha_ini + ' Al: ' + fecha_fin
    Story.append(Paragraph(fecha_reporte, style_punto))
    # Story.append(tabla_datos)
    ciudad_actual = ''
    sucursal_actual = ''
    codigo_moneda = 'Bs.'
    punto_id = ''
    datos_tabla = []
    data = []
    filas = 0
    total = 0
    descuento = 0
    subtotal = 0
    adicional = 0
    en_ingresos = 0
    bande = 0
    titulo_punto = ''

    for dato in datos_reporte:

        # punto
        if punto_id != dato['punto']:
            bande += 1
            # primera vuelta, no se cierra tabla
            if bande > 1:
                # cerramos tabla anterior y aniadimos
                if len(data) > 0:
                    datos_tabla = ['', '', '', 'Totales: ', str(subtotal), str(descuento), str(adicional), str(total), str(en_ingresos)]
                    data.append(datos_tabla)

                    # ancho columnas
                    tabla_datos = Table(data, colWidths=[22*mm, 12*mm, 58*mm, 25*mm, 17*mm, 15*mm, 17*mm, 17*mm, 17*mm], repeatRows=1)
                    tabla_datos.setStyle(TableStyle([('BACKGROUND', (0, 0), (8, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                                     ('ALIGN', (4, 0), (8, filas+1), 'RIGHT'),
                                                     #('ALIGN', (1, 0), (1, filas+1), 'RIGHT'),
                                                     #('ALIGN', (5, filas+1), (5, filas+1), 'RIGHT'),
                                                     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                                     ('FONTSIZE', (0, 0), (8, 0), 10),
                                                     ('FONTSIZE', (0, 1), (-1, -1), 9),
                                                     ('FONTNAME', (0, 0), (8, 0), 'Helvetica'),
                                                     ('FONTNAME', (0, 1), (8, filas), 'Helvetica'),
                                                     ('FONTNAME', (0, filas+1), (8, filas+1), 'Helvetica-Bold'),
                                                     ('LEFTPADDING', (0, 0), (-1, -1), 2),
                                                     ('RIGHTPADDING', (0, 1), (-1, -1), 1),
                                                     ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                                                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
                    # aniadimos la tabla
                    Story.append(Paragraph(titulo_punto, style_punto))
                    Story.append(tabla_datos)
                    Story.append(Spacer(100*mm, 5*mm))

            # texto nombre de la caja
            #Story.append(Paragraph(dato['punto'] + ' - ' + dato['caja'], style_punto))
            titulo_punto = dato['punto']
            punto_id = dato['punto']

            # creamos tabla para esta caja
            data = []

            data.append(['Fecha', 'N.', 'Cliente', 'Tipo', 'SubT', 'Desc', 'Ad.', 'Total', 'Ingr.'])
            filas = 0
            total = 0
            subtotal = 0
            descuento = 0
            adicional = 0
            en_ingresos = 0

        # seguimos llenando de datos la tabla hasta cambiar de caja, sucursal o ciudad
        cliente = Paragraph(dato['cliente'])
        tipo = Paragraph(dato['tipo'])

        datos_tabla = [dato['fecha'], str(dato['numero_contrato'])+' ', cliente, tipo, str(dato['subtotal']), str(dato['descuento']),
                       str(dato['adicional']), str(dato['total']+dato['adicional']), str(dato['ingresos_caja'])]
        data.append(datos_tabla)
        filas += 1

        descuento += dato['descuento']
        subtotal += dato['subtotal']
        adicional += dato['adicional']
        total += dato['total'] + dato['adicional']
        en_ingresos += dato['ingresos_caja']

        # codigo moneda para los totales
        # if codigo_moneda != dato['tipo_moneda']:
        #     codigo_moneda = dato['tipo_moneda']

        # titulo de ciudad, despues que se terminen las tablas
        if ciudad_actual != dato['ciudad']:
            Story.append(Paragraph(dato['ciudad'], style_ciudad))
            ciudad_actual = dato['ciudad']

        # titulo sucursal despues que se termine de dibujar las tablas
        if sucursal_actual != dato['sucursal']:
            Story.append(Paragraph(dato['sucursal'], style_sucursal))
            sucursal_actual = dato['sucursal']

    # datos de la ultima tabla
    if len(data) > 0:
        datos_tabla = ['', '', '', 'Totales: ', str(subtotal), str(descuento), str(adicional), str(total), str(en_ingresos)]
        data.append(datos_tabla)

        tabla_datos = Table(data, colWidths=[22*mm, 12*mm, 58*mm, 25*mm, 17*mm, 15*mm, 17*mm, 17*mm, 17*mm], repeatRows=1)
        tabla_datos.setStyle(TableStyle([('BACKGROUND', (0, 0), (8, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                         ('ALIGN', (4, 0), (8, filas+1), 'RIGHT'),
                                         #('ALIGN', (1, 0), (1, filas+1), 'RIGHT'),
                                         #('ALIGN', (5, filas+1), (5, filas+1), 'RIGHT'),
                                         ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                         ('FONTSIZE', (0, 0), (8, 0), 10),
                                         ('FONTSIZE', (0, 1), (-1, -1), 9),
                                         ('FONTNAME', (0, 0), (8, 0), 'Helvetica'),
                                         ('FONTNAME', (0, 1), (8, filas), 'Helvetica'),
                                         ('FONTNAME', (0, filas+1), (8, filas+1), 'Helvetica-Bold'),
                                         ('LEFTPADDING', (0, 0), (-1, -1), 2),
                                         ('RIGHTPADDING', (0, 1), (-1, -1), 1),
                                         ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                                         ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
        # aniadimos la tabla
        Story.append(Paragraph(titulo_punto, style_punto))
        Story.append(tabla_datos)

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
