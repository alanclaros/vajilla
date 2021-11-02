from reportlab.lib.units import mm


def cabecera(canvas, posY=270.5, **datos):
    altoTxt = 13

    textobject = canvas.beginText()
    textobject.setTextOrigin(5*mm, posY*mm)
    textobject.setFont("Helvetica", 12)
    textobject.setFillColorRGB(0, 0, 0)

    # dibujamos
    # empresa
    textobject.textOut(datos['empresa'])
    # direccion
    textobject.setFont("Helvetica", 11)
    textobject.moveCursor(0, altoTxt)
    textobject.textOut(datos['direccion'])
    # ciudad
    textobject.setFont("Helvetica", 10)
    textobject.moveCursor(0, altoTxt)
    textobject.textOut(datos['ciudad'])
    # telefonos
    textobject.moveCursor(0, altoTxt)
    textobject.textOut(datos['telefonos'])
    # actividad
    textobject.setFont("Helvetica-Oblique", 8)
    textobject.moveCursor(0, altoTxt)
    textobject.textOut(datos['actividad'])

    # titulo
    textobject.setFont("Helvetica", 12)
    textobject.moveCursor(240, -(2*altoTxt))
    textobject.textOut(datos['titulo'])

    if posY == 270.5:
        # hoja vertical
        # logo
        canvas.drawImage(datos['logo'], 190*mm, (posY-12.5)*mm, width=50, height=50)

        # fecha impresion
        textobject.setFont("Helvetica", 9)
        textobject.moveCursor(265, (2*altoTxt))
        textobject.textOut(datos['fecha_impresion'])
    else:
        # hoja horizontal
        # logo
        canvas.drawImage(datos['logo'], 250*mm, (posY-12.5)*mm, width=50, height=50)

        # fecha impresion
        textobject.setFont("Helvetica", 9)
        textobject.moveCursor(425, (2*altoTxt))
        textobject.textOut(datos['fecha_impresion'])

    # lineas
    # titulo
    canvas.line(85*mm, (posY-12.5)*mm, 165*mm, (posY-12.5)*mm)

    # output
    canvas.drawText(textobject)
