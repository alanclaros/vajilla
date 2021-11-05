from django.apps.registry import apps
from reportlab.lib.pagesizes import letter
from reportlab.lib import pagesizes
# from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

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
    # total
    canvas.drawString(posX2*mm, posY*mm, ' ')
    canvas.drawRightString(posX2*mm, posY*mm, "Total : ")
    canvas.drawString(posX3*mm, posY*mm, ' ')
    canvas.drawRightString(posX3*mm, posY*mm, str(venta.total) + ' Bs.')

    # fecha evento
    posY = posY - altoTxt
    canvas.drawString(posX*mm, posY*mm, get_date_show(fecha=venta.fecha_devolucion, formato='dd-MMM-yyyy HH:ii'))
    canvas.drawRightString(posX*mm, posY*mm, "F. Devol. : ")

    # pie de pagina
    canvas.setFont('Times-Italic', 8)
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))

    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()

    canvas.setFont('Times-Italic', 8)
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))
    canvas.restoreState()


def rptVentasResumen(buffer_pdf, usuario, venta_id):

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

    global DATO_REGISTRO, RPT_CONTRATO, RPT_ESTADO
    DATO_REGISTRO = str(venta.venta_id)
    RPT_CONTRATO = venta.numero_contrato
    RPT_ESTADO = 'PREVENTA'

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
    Story.append(Spacer(100*mm, 65*mm))

    # tabla
    datos_tabla = []
    data = []
    data.append(['Fecha', 'Operacion', 'Monto', 'Saldo'])
    filas = 0
    saldo_venta = venta.total

    # gastos
    status_activo = apps.get_model('status', 'Status').objects.get(pk=1)
    status_anulado = apps.get_model('status', 'Status').objects.get(pk=settings.STATUS_ANULADO)
    cajas_egresos = apps.get_model('cajas', 'CajasEgresos').objects.filter(venta_id=venta.venta_id, status_id=status_activo).order_by('fecha')

    for egreso in cajas_egresos:
        concepto = Paragraph('Gasto, ' + egreso.concepto, style_tabla_datos)
        saldo_venta = saldo_venta + egreso.monto
        dato_add = [get_date_show(fecha=egreso.fecha, formato='dd-MMM-yyyy HH:ii'), concepto, str(round(egreso.monto, 2)), str(round(saldo_venta, 2))]
        data.append(dato_add)
        filas += 1

    # devolucion de productos y aumentos
    deuda_detalles = 0
    for detalle in ventas_detalles:
        deuda_detalles += detalle.total_vuelta_rotura

    # aumentos
    filtro_aumento = {}
    filtro_aumento['venta_id'] = venta
    ventas_aumentos = VentasAumentos.objects.filter(**filtro_aumento).exclude(status_id=status_anulado)
    for ve_aumento in ventas_aumentos:
        ventas_aumentos_detalles = VentasAumentosDetalles.objects.filter(venta_aumento_id=ve_aumento)
        for detalle in ventas_aumentos_detalles:
            deuda_detalles += detalle.total_vuelta_rotura

    # rotura y refaccion
    saldo_venta = saldo_venta + deuda_detalles
    dato_add = ['', 'Refaccion y Reposicion de Productos', str(round(deuda_detalles, 2)), str(round(saldo_venta, 2))]
    data.append(dato_add)
    filas += 1

    # ingresos efectivo
    lista_ingresos = apps.get_model('cajas', 'CajasIngresos').objects.filter(venta_id=venta.venta_id, status_id=status_activo).order_by('fecha')
    for ingreso in lista_ingresos:
        concepto = Paragraph('Cobro, ' + ingreso.concepto, style_tabla_datos)
        saldo_venta = saldo_venta - ingreso.monto
        dato_add = [get_date_show(fecha=ingreso.fecha, formato='dd-MMM-yyyy HH:ii'), concepto, str(round(ingreso.monto, 2)), str(round(saldo_venta, 2))]
        data.append(dato_add)
        filas += 1

    tabla_datos = Table(data, colWidths=[28*mm, 130*mm, 14*mm, 16*mm], repeatRows=1)
    num_cols = 4-1
    align_right_from = 2

    tabla_datos.setStyle(TableStyle([('BACKGROUND', (0, 0), (num_cols, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                     ('ALIGN', (align_right_from, 0), (num_cols, filas), 'RIGHT'),
                                     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                     ('FONTSIZE', (0, 0), (num_cols, 0), 9),
                                     ('FONTSIZE', (0, 1), (num_cols, filas), 8),
                                     ('FONTNAME', (0, 0), (num_cols, 0), 'Helvetica'),
                                     ('FONTNAME', (0, 1), (num_cols, filas), 'Helvetica'),
                                     ('FONTNAME', (num_cols, filas), (num_cols, filas), 'Helvetica-Bold'),
                                     ('LEFTPADDING', (0, 0), (-1, -1), 2),
                                     ('RIGHTPADDING', (0, 1), (-1, -1), 1),
                                     ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))

    # aniadimos la tabla

    Story.append(tabla_datos)

    # firmas
    # Story.append(Spacer(100*mm, 15*mm))
    # datos_firmas = [['_____________________', '__________________'], ['Entregue Conforme', 'Recibi Conforme'], [venta.user_perfil_id.user_id.username, '']]
    # tabla_firmas = Table(datos_firmas, colWidths=[90*mm, 90*mm], repeatRows=0)
    # tabla_firmas.setStyle(TableStyle([
    #                                  ('ALIGN', (0, 0), (1, 2), 'CENTER'),
    #                                  #('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    #                                  ('FONTSIZE', (0, 0), (1, 2), 10),
    #                                  ('FONTNAME', (0, 0), (1, 2), 'Helvetica'),
    #                                  ('LEFTPADDING', (0, 0), (-1, -1), 2),
    #                                  ('RIGHTPADDING', (0, 1), (-1, -1), 1),
    #                                  ('VALIGN', (0, 1), (-1, -1), 'TOP'),
    #                                  ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
    # Story.append(tabla_firmas)

    # creamos
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
