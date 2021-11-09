from django.apps.registry import apps
from reportlab.lib.pagesizes import letter
from reportlab.lib import pagesizes
#from reportlab.pdfgen import canvas
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
#from controllers.reportes.ReportesController import ReportesController
from controllers.ventas.VentasController import VentasController

import os

# tamanio de pagina
pagesize = pagesizes.portrait(pagesizes.letter)
RPT_SUCURSAL_ID = 0
DATO_CAJA = ''


def myFirstPage(canvas, doc):
    canvas.saveState()

    datosReporte = get_sucursal_settings(RPT_SUCURSAL_ID)
    datosReporte['titulo'] = 'Stock de Productos ' + DATO_CAJA
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


def rptStockProductos(buffer_pdf, usuario, linea_id, almacen_id, fecha_ini, fecha_fin):
    # pdf
    #pdf = canvas.Canvas(buffer, pagesize=letter)

    # datos sucursal
    user_perfil = UsersPerfiles.objects.get(user_id=usuario)
    #permisos = get_permisos_usuario(usuario, settings.MOD_REPORTES)
    punto = Puntos.objects.get(pk=user_perfil.punto_id)
    sucursal_id_user = punto.sucursal_id.sucursal_id
    global RPT_SUCURSAL_ID
    RPT_SUCURSAL_ID = sucursal_id_user

    styles = getSampleStyleSheet()
    # personalizamos
    style_almacen = ParagraphStyle('almacen',
                                   fontName="Helvetica-Bold",
                                   fontSize=12,
                                   parent=styles['Normal'],
                                   alignment=1,
                                   spaceAfter=10)

    doc = SimpleDocTemplate(buffer_pdf, pagesize=letter, leftMargin=10 * mm, rightMargin=10 * mm, topMargin=10 * mm, bottomMargin=15 * mm)

    """datos del reporte"""
    #reporte_controller = ReportesController()
    #datos_reporte = reporte_controller.datos_stock_productos(usuario, linea_id=linea_id, almacen_id=almacen_id)
    venta_controller = VentasController()
    datos_stock = venta_controller.stock_productos(fecha_entrega=fecha_ini, fecha_devolucion=fecha_fin, formato='dd-MMM-yyyy')
    lista_productos = apps.get_model('productos', 'Productos').objects.filter(status_id=venta_controller.status_activo).order_by('linea_id__linea', 'producto')
    datos_reporte = []
    valor_linea = int(linea_id)
    for li_pro in lista_productos:
        entra = 'si'
        if valor_linea != 0:
            if valor_linea != li_pro.linea_id.linea_id:
                entra = 'no'
        if entra == 'si':
            dato_add = {}
            dato_add['linea'] = li_pro.linea_id.linea
            dato_add['producto'] = li_pro.producto
            cantidad = datos_stock[li_pro.producto_id]
            dato_add['cantidad'] = cantidad

            datos_reporte.append(dato_add)

    # print(datos_reporte)

    Story = []
    Story.append(Spacer(100*mm, 22*mm))

    almacen_actual = ''
    datos_tabla = []
    data = []
    filas = 0

    data.append(['Producto', 'Cantidad'])
    for dato in datos_reporte:
        linea = Paragraph(dato['linea'])
        producto = Paragraph(dato['producto'])
        datos_tabla = [producto, str(dato['cantidad'])]

        data.append(datos_tabla)
        filas += 1

    num_cols = 2-1
    align_right_from = 1

    tabla_datos = Table(data, colWidths=[175*mm, 20*mm], repeatRows=1)
    tabla_datos.setStyle(TableStyle([('BACKGROUND', (0, 0), (num_cols, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                     ('ALIGN', (align_right_from, 0), (num_cols, filas), 'RIGHT'),
                                     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                     ('FONTSIZE', (0, 0), (num_cols, 0), 10),
                                     ('FONTSIZE', (0, 1), (-1, -1), 9),
                                     ('FONTNAME', (0, 0), (num_cols, 0), 'Helvetica'),
                                     ('FONTNAME', (0, 1), (num_cols, filas), 'Helvetica'),
                                     ('LEFTPADDING', (0, 0), (-1, -1), 2),
                                     ('RIGHTPADDING', (0, 1), (-1, -1), 1),
                                     ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
    # aniadimos la tabla
    Story.append(Paragraph(almacen_actual, style_almacen))
    Story.append(tabla_datos)
    Story.append(Spacer(100*mm, 5*mm))

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
