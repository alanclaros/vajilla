from django.apps.registry import apps
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib import pagesizes
# from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm

from datetime import datetime

from reportlab.pdfbase.pdfmetrics import stringWidth

# imagen
from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# cabecera
from reportes.cabecera import cabecera

# modelos
from ventas.models import Ventas, VentasDetalles, VentasAumentos, VentasAumentosDetalles

# settings
from django.conf import settings

# utils
from utils.permissions import get_sucursal_settings, report_date
from utils.dates_functions import get_date_show

import os
import copy

# tamanio de pagina
pagesize = pagesizes.portrait(pagesizes.letter)
# pagesize = pagesizes.landscape(pagesizes.letter)
RPT_SUCURSAL_ID = 0
DATO_REGISTRO = ''
RPT_CONTRATO = '#'
RPT_ESTADO = 'preventa'
RPT_ANULADO = ''

# aumento para la direccion y la observacion
AUMENTO_Y = 0


def myFirstPage(canvas, doc):
    canvas.saveState()

    datosReporte = get_sucursal_settings(RPT_SUCURSAL_ID)
    datosReporte['titulo'] = 'Venta, ' + DATO_REGISTRO
    datosReporte['fecha_impresion'] = report_date()
    dir_img = os.path.join(settings.STATIC_ROOT, 'img/logo.png')
    datosReporte['logo'] = dir_img

    # para horizontal
    # posicionY = 207
    # cabecera(canvas, posY=posicionY, **datosReporte)

    # vertical
    cabecera(canvas=canvas, **datosReporte)

    # cabecera
    posY = 244
    altoTxt = 6
    posX = 30
    posX2 = 160
    posX3 = 184

    venta = Ventas.objects.get(pk=int(DATO_REGISTRO))

    # estado de la venta
    estado_venta = 'PREVENTA'
    if venta.status_id.status_id == settings.STATUS_VENTA:
        estado_venta = 'VENTA'
    if venta.status_id.status_id == settings.STATUS_SALIDA_ALMACEN:
        estado_venta = 'SALIDA'
    if venta.status_id.status_id == settings.STATUS_VUELTA_ALMACEN:
        estado_venta = 'VUELTA'
    if venta.status_id.status_id == settings.STATUS_FINALIZADO:
        estado_venta = 'FINALIZADO'
    if venta.status_id.status_id == settings.STATUS_ANULADO:
        estado_venta = 'ANULADO'

    canvas.setFont("Helvetica", 10)
    # contrato
    canvas.setStrokeColorRGB(220/255, 220/255, 220/255)
    canvas.setFillColorRGB(240/255, 240/255, 240/255)
    canvas.rect(29.5*mm, 243*mm, 30*mm, 5*mm, fill=1)
    # estado
    canvas.rect(132*mm, 243*mm, 30*mm, 5*mm, fill=1)
    # total
    canvas.rect(159.5*mm, 213*mm, 25*mm, 5*mm, fill=1)
    canvas.setStrokeColorRGB(0, 0, 0)
    canvas.setFillColorRGB(0, 0, 0)

    canvas.drawString(posX*mm, posY*mm, '# ' + venta.numero_contrato)
    canvas.drawRightString(posX*mm, posY*mm, "Contrato : ")
    # estado venta
    canvas.drawString(posX2*mm, posY*mm, ' ')
    canvas.drawRightString(posX2*mm, posY*mm, estado_venta)
    #canvas.drawString(posX3*mm, posY*mm, ' ')
    #canvas.drawRightString(posX3*mm, posY*mm, str(venta.subtotal) + ' Bs.')

    # cliente
    posY = posY - altoTxt
    canvas.drawString(posX*mm, posY*mm, venta.apellidos + ' ' + venta.nombres)
    canvas.drawRightString(posX*mm, posY*mm, "Cliente : ")
    # subtotal
    canvas.drawString(posX2*mm, posY*mm, ' ')
    canvas.drawRightString(posX2*mm, posY*mm, "Subtotal : ")
    canvas.drawString(posX3*mm, posY*mm, ' ')
    canvas.drawRightString(posX3*mm, posY*mm, str(venta.subtotal) + ' Bs.')

    # ci nit
    posY = posY - altoTxt
    canvas.drawString(posX*mm, posY*mm, venta.ci_nit)
    canvas.drawRightString(posX*mm, posY*mm, "CI/NIT : ")
    # descuento
    #canvas.drawString(posX2*mm, posY*mm, '-' + str(venta.descuento) + ' Bs.')
    canvas.drawString(posX2*mm, posY*mm, ' ')
    canvas.drawRightString(posX2*mm, posY*mm, "Desc. : ")
    canvas.drawString(posX3*mm, posY*mm, ' ')
    canvas.drawRightString(posX3*mm, posY*mm, '-' + str(venta.descuento) + ' Bs.')

    # telefonos
    posY = posY - altoTxt
    canvas.drawString(posX*mm, posY*mm, venta.telefonos)
    canvas.drawRightString(posX*mm, posY*mm, "Fonos : ")
    # costo transporte
    canvas.drawString(posX2*mm, posY*mm, ' ')
    canvas.drawRightString(posX2*mm, posY*mm, "Transporte : ")
    canvas.drawString(posX3*mm, posY*mm, ' ')
    canvas.drawRightString(posX3*mm, posY*mm, '+' + str(venta.costo_transporte) + ' Bs.')

    # fecha evento
    posY = posY - altoTxt
    canvas.drawString(posX*mm, posY*mm, get_date_show(venta.fecha_evento))
    canvas.drawRightString(posX*mm, posY*mm, "F. Evento : ")
    # garantia
    canvas.drawString(posX2*mm, posY*mm, ' ')
    canvas.drawRightString(posX2*mm, posY*mm, "Garantia : ")
    canvas.drawString(posX3*mm, posY*mm, ' ')
    canvas.drawRightString(posX3*mm, posY*mm, '+' + str(venta.garantia_bs) + ' Bs.')

    # fecha entrega
    posY = posY - altoTxt
    canvas.drawString(posX*mm, posY*mm, get_date_show(fecha=venta.fecha_entrega, formato='dd-MMM-yyyy HH:ii'))
    canvas.drawRightString(posX*mm, posY*mm, "F. Entrega : ")
    # garantia
    canvas.drawString(posX2*mm, posY*mm, ' ')
    canvas.drawRightString(posX2*mm, posY*mm, "Total : ")
    canvas.drawString(posX3*mm, posY*mm, ' ')
    canvas.drawRightString(posX3*mm, posY*mm, str(venta.garantia_bs + venta.total) + ' Bs.')

    # fecha evento
    posY = posY - altoTxt
    canvas.drawString(posX*mm, posY*mm, get_date_show(fecha=venta.fecha_devolucion, formato='dd-MMM-yyyy HH:ii'))
    canvas.drawRightString(posX*mm, posY*mm, "F. Devol. : ")

    # direccion
    # posY = posY - altoTxt
    # canvas.drawString(posX*mm, posY*mm, venta.direccion_evento)
    # canvas.drawRightString(posX*mm, posY*mm, "Direccion : ")

    # observacion
    posY = posY - altoTxt
    # canvas.drawString(posX*mm, posY*mm, venta.observacion)
    # canvas.drawRightString(posX*mm, posY*mm, "Obs. : ")

    width = 200*mm
    height = 100*mm

    styles = getSampleStyleSheet()
    style_tabla = ParagraphStyle('tabla_head',
                                 fontName="Helvetica",
                                 fontSize=9,
                                 parent=styles['Normal'],
                                 alignment=0,
                                 spaceAfter=0)

    observacion = Paragraph(venta.observacion, style_tabla)
    direccion_evento = Paragraph(venta.direccion_evento, style_tabla)

    data = [['Direccion : ', direccion_evento], ['Obs : ', observacion]]

    f = Table(data, colWidths=[20*mm, 180*mm], repeatRows=1)
    f.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
        ('ALIGN', (0, 1), (0, 1), 'RIGHT'),
        #('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
        ('RIGHTPADDING', (0, 0), (-1, -1), 1),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
    f.wrapOn(canvas, width, height)
    x = (posX-20)*mm
    y = (posY-(8+AUMENTO_Y))*mm
    f.drawOn(canvas, x, y)

    # pie de pagina
    canvas.setFont('Times-Italic', 8)
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))

    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()

    canvas.setFont('Times-Italic', 8)
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))
    canvas.restoreState()


def rptVentasConCostos(buffer_pdf, usuario, venta_id):

    # datos sucursal
    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=usuario)
    punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)
    sucursal_id_user = punto.sucursal_id.sucursal_id
    global RPT_SUCURSAL_ID
    RPT_SUCURSAL_ID = sucursal_id_user

    # venta
    venta = Ventas.objects.get(pk=venta_id)
    ventas_detalles = VentasDetalles.objects.select_related('producto_id').filter(venta_id=venta).order_by('producto_id__producto')

    # verificamos si esta anulado
    dato_anulado = ''
    if venta.status_id.status_id == settings.STATUS_ANULADO:
        usuario_perfil_anula = apps.get_model('permisos', 'UsersPerfiles').objects.get(pk=venta.user_perfil_id_anula)
        motivo_anula = venta.motivo_anula
        dato_anulado = usuario_perfil_anula.user_id.username + ', ' + motivo_anula

    global DATO_REGISTRO, RPT_CONTRATO, RPT_ESTADO, RPT_ANULADO, AUMENTO_Y
    DATO_REGISTRO = str(venta.venta_id)
    RPT_CONTRATO = venta.numero_contrato
    RPT_ESTADO = 'PREVENTA'

    if len(venta.observacion) > 120 and len(venta.direccion_evento) > 120:
        AUMENTO_Y = 8
    elif len(venta.observacion) > 120 or len(venta.direccion_evento) > 120:
        AUMENTO_Y = 4
    else:
        AUMENTO_Y = 0

    if venta.status_id.status_id == settings.STATUS_VENTA:
        RPT_ESTADO = 'VENTA'
    if venta.status_id.status_id == settings.STATUS_SALIDA_ALMACEN:
        RPT_ESTADO = 'SALIDA'
    if venta.status_id.status_id == settings.STATUS_VUELTA_ALMACEN:
        RPT_ESTADO = 'VUELTA'
    if venta.status_id.status_id == settings.STATUS_FINALIZADO:
        RPT_ESTADO = 'FINALIZADO'
    RPT_ANULADO = dato_anulado

    styles = getSampleStyleSheet()
    # personalizamos
    style_tabla_datos = ParagraphStyle('tabla_datos',
                                       fontName="Helvetica",
                                       fontSize=8,
                                       parent=styles['Normal'],
                                       alignment=0,
                                       spaceAfter=0)

    style_firmas = ParagraphStyle('firmas',
                                  fontName="Helvetica",
                                  fontSize=10,
                                  parent=styles['Normal'],
                                  alignment=0,
                                  spaceAfter=0)

    # hoja vertical
    doc = SimpleDocTemplate(buffer_pdf, pagesize=letter, leftMargin=10 * mm, rightMargin=10 * mm, topMargin=10 * mm, bottomMargin=15 * mm)

    # hoja horizontal
    # doc = SimpleDocTemplate(buffer_pdf, pagesize=landscape(letter), leftMargin=10 * mm, rightMargin=10 * mm, topMargin=10 * mm, bottomMargin=15 * mm)

    # armamos
    Story = []
    if RPT_ANULADO == '':
        Story.append(Spacer(100*mm, 79*mm))
    else:
        Story.append(Spacer(100*mm, 84*mm))

    if AUMENTO_Y == 4:
        Story.append(Spacer(100*mm, 4*mm))
    if AUMENTO_Y == 8:
        Story.append(Spacer(100*mm, 8*mm))

    # tabla
    datos_tabla = []
    data = []
    data.append(['Producto', 'Salida', 'Costo', 'Total', 'Vuelta', 'Rotura', 'Refacc', 'Vuelta'])

    filas = 0
    total = 0
    total_vuelta = 0

    # detalles
    productos_detalles = []
    for detalle in ventas_detalles:
        dato = {}
        dato['producto_id'] = detalle.producto_id.producto_id
        dato['producto'] = detalle.producto_id.producto
        dato['cantidad_salida'] = detalle.cantidad_salida
        dato['costo_salida'] = detalle.costo_salida
        dato['total_salida'] = detalle.total_salida
        dato['cantidad_vuelta'] = detalle.cantidad_vuelta
        dato['costo_total_rotura'] = detalle.costo_total_rotura
        dato['costo_refaccion'] = detalle.costo_refaccion
        dato['total_vuelta_rotura'] = detalle.total_vuelta_rotura
        productos_detalles.append(dato)

    # aumentamos las cantidades de salida de los aumentos
    # filtro_va= {}
    # filtro_va['venta_id']= venta
    # filtro_va['status_id__in']= [settings.STATUS_VENTA, settings.STATUS_]
    ventas_aumentos = VentasAumentos.objects.filter(venta_id=venta).exclude(status_id__status_id=settings.STATUS_ANULADO)
    for va_aumento in ventas_aumentos:
        ventas_aumentos_detalles = VentasAumentosDetalles.objects.filter(venta_aumento_id=va_aumento)
        for va_detalle in ventas_aumentos_detalles:
            existe = -1
            pos = 0
            for pro_de in productos_detalles:
                if pro_de['producto_id'] == va_detalle.producto_id.producto_id:
                    existe = pos
                pos += 1

            #print('existe...: ', existe, ' productos detalles: ', productos_detalles)
            if existe > -1:
                # print('pos cero...: ', productos_detalles[])
                productos_detalles[existe]['cantidad_salida'] = productos_detalles[existe]['cantidad_salida'] + va_detalle.cantidad_salida
            else:
                dato = {}
                dato['producto_id'] = va_detalle.producto_id.producto_id
                dato['producto'] = va_detalle.producto_id.producto
                dato['cantidad_salida'] = va_detalle.cantidad_salida
                dato['costo_salida'] = va_detalle.costo_salida
                dato['total_salida'] = va_detalle.total_salida
                dato['cantidad_vuelta'] = va_detalle.cantidad_vuelta
                dato['costo_total_rotura'] = va_detalle.costo_total_rotura
                dato['costo_refaccion'] = va_detalle.costo_refaccion
                dato['total_vuelta_rotura'] = va_detalle.total_vuelta_rotura
                productos_detalles.append(dato)

    #print('productos....: ', productos_detalles)

    # cargamos los registros
    for detalle in productos_detalles:
        producto = Paragraph(detalle['producto'], style_tabla_datos)
        datos_tabla = []

        datos_tabla = [producto, str(int(detalle['cantidad_salida'])), str(round(detalle['costo_salida'], 2)), str(round(detalle['total_salida'], 2)),
                       str(int(detalle['cantidad_vuelta'])), str(round(detalle['costo_total_rotura'], 2)), str(round(detalle['costo_refaccion'])), str(round(detalle['total_vuelta_rotura']))]
        data.append(datos_tabla)
        filas += 1
        total += detalle['total_salida']
        total_vuelta += detalle['total_vuelta_rotura']

    # aniadimos la tabla
    datos_tabla = ['', '', 'Total: ', str(round(total, 2)), '', '', 'Total: ', str(round(total_vuelta, 2))]
    data.append(datos_tabla)

    tabla_datos = Table(data, colWidths=[110*mm, 12*mm, 12*mm, 15*mm, 12*mm, 12*mm, 13*mm, 15*mm], repeatRows=1)
    num_cols = 8-1
    align_right_from = 1

    tabla_datos.setStyle(TableStyle([('BACKGROUND', (0, 0), (num_cols, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                     # ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                                     ('ALIGN', (align_right_from, 0), (num_cols, filas+1), 'RIGHT'),
                                     #('ALIGN', (5, filas+1), (6, filas+1), 'RIGHT'),
                                     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                     ('FONTSIZE', (0, 0), (num_cols, 0), 9),
                                     ('FONTSIZE', (0, 1), (num_cols, filas+1), 8),
                                     ('FONTNAME', (0, 0), (num_cols, 0), 'Helvetica'),
                                     ('FONTNAME', (0, 1), (num_cols, filas), 'Helvetica'),
                                     ('FONTNAME', (0, filas+1), (num_cols, filas+1), 'Helvetica-Bold'),
                                     ('LEFTPADDING', (0, 0), (-1, -1), 2),
                                     ('RIGHTPADDING', (0, 1), (-1, -1), 1),
                                     ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))

    # aniadimos la tabla

    Story.append(tabla_datos)
    Story.append(Spacer(100*mm, 15*mm))
    datos_firmas = [['_____________________', '__________________'], ['Entregue Conforme', 'Recibi Conforme'], [venta.user_perfil_id.user_id.username, '']]
    tabla_firmas = Table(datos_firmas, colWidths=[90*mm, 90*mm], repeatRows=0)
    tabla_firmas.setStyle(TableStyle([
                                     ('ALIGN', (0, 0), (1, 2), 'CENTER'),
                                     #('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                     ('FONTSIZE', (0, 0), (1, 2), 10),
                                     ('FONTNAME', (0, 0), (1, 2), 'Helvetica'),
                                     ('LEFTPADDING', (0, 0), (-1, -1), 2),
                                     ('RIGHTPADDING', (0, 1), (-1, -1), 1),
                                     ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
    Story.append(tabla_firmas)
    # Story.append(Spacer(100*mm, 5*mm))

    # creamos
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
