import os
import configparser

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import red
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Frame, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)


class ImpresionComprobante:
    def _propiedades(self):
        self._autor = 'Enrique Santana Anaya'
        self._titulo = 'Representación impresa de un CFDI'
        self._pdf_titulo = 'Comprobante Físcal'
        self._creador = 'ProLeCSA'

    def _datos_pie(self):
        self._info_extra = [
            [self._comprobante.total_letra, '', '', ''],
            [
                'Forma de pago:',
                self._comprobante.forma_pago,
                'Número de Cuenta:',
                self._comprobante.cuenta_pago,
            ],
            [
                'Uso de CFDI:',
                self._comprobante.receptor.uso_cfdi,
                'Tipo de Comprobante:',
                self._comprobante.tipo_comprobante,
            ],
            [
                'Método de pago:',
                self._comprobante.metodo_pago,
            ],
        ]
        subtotal = float(self._comprobante.subtotal)
        total = float(self._comprobante.total)
        impuestos = total - subtotal
        self._info_totales = [
            ['Subtotal :', f'${subtotal:,.2f}'],
            ['I.V.A. 0.16% :', f'${impuestos:,.2f}'],
            ['Total :', f'${total:,.2f}'],
        ]

    def _rutas(self):
        self.nombre = os.path.join(
            'facturaciononline',
            'static',
            'facturas',
            self._comprobante.fecha[5:7] + self._comprobante.fecha[:4],
            self._comprobante.nombre_archivo[:-4] + '.pdf'
        )
        self._ruta_logos = ''
        self._archivo_logo = ''
        self._codigo_color_lineas = ''

    def __init__(self, comprobante):
        self._comprobante = comprobante
        self._styles = getSampleStyleSheet()
        self._propiedades()
        self._rutas()
        self.resuelve_codigos()

    @property
    def comprobante(self):
        return self._comprobante

    @comprobante.setter
    def comprobante(self, comprobante):
        self._comprobante = comprobante

    @property
    def ruta_logos(self):
        return self._ruta_logos

    @ruta_logos.setter
    def ruta_logos(self, ruta_logos):
        self._ruta_logos = ruta_logos

    @property
    def archivo_logo(self):
        return self._archivo_logo

    @archivo_logo.setter
    def archivo_logo(self, archivo_logo):
        self._archivo_logo = archivo_logo

    @property
    def codigo_color_lineas(self):
        return self._codigo_color_lineas

    @codigo_color_lineas.setter
    def codigo_color_lineas(self, codigo_color_lineas):
        self._codigo_color_lineas = codigo_color_lineas

    def _lee_ini(self):
        config = configparser.ConfigParser()
        config.read(
            os.path.join('facturaciononline', 'static', 'recursos',
                         'layout.ini'),
            encoding='utf-8'
        )
        self._ruta_logos = config['Configuracion'].get('ruta_logos').split('|')
        if self._comprobante.emisor.rfc in config:
            emisor = config[self._comprobante.emisor.rfc]
            self._comprobante.emisor.calle_numero = emisor.get('CN')
            self._comprobante.emisor.colonia = emisor.get('C')
            self._comprobante.emisor.ciudad = emisor.get('CD')
            self._comprobante.emisor.estado_pais = emisor.get('EP')
            self._comprobante.emisor.codigo_postal = emisor.get('CP')
            self._archivo_logo = emisor.get('LG')
            self._codigo_color_lineas = emisor.get('CL')

    def _propiedades_canvas(self, canvas):
        canvas.setAuthor(self._autor)
        canvas.setTitle(self._titulo)
        canvas.setSubject(self._pdf_titulo)
        canvas.setCreator(self._creador)
        return canvas
    def _set_tamanos(self):
        self._small = ParagraphStyle('Pequeña')
        self._small.fontSize = 7
        self._small.leading = 7
        self._small.splitLongWords = True
        self._small.spaceShrinkage = 0.05

    def _set_estilos(self):
        self._estilo_tabla_titulos = TableStyle([
            ('LEFTPADDING', (1, 0), (-1, -1), 4),
        ])
        self._estilo_tabla_doc = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 1), (0, 1), red),
            ('SIZE', (0, 7), (0, 7), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 7), (0, 7), 8),
        ])
        self._estilo_tabla_info = TableStyle([
            ('SIZE', (0, 0), (-1, -1), 8),
            ('LEADING', (0, 0), (-1, -1), 5.7),
            ('SPAN', (0, 0), (3, 0)),
        ])
        self._estilo_tabla_totales = TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LEADING', (0, 0), (-1, -1), 5.7),
        ])
        self._estilo_tabla_info_qr = TableStyle([
            ('SIZE', (0, 0), (-1, -1), 8),
            ('LEADING', (0, 0), (-1, -1), 5.7),
        ])
        self._estilo_seg_cab = TableStyle([
            ('LEADING', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
        ])

    def _set_marcos(self, canvas):
        rojo, verde, azul = self._codigo_color_lineas[1:-1].split(',')
        # Marcos
        canvas.setStrokeColorRGB(float(rojo), float(verde), float(azul))
        # Marcos Cabecera
        canvas.roundRect(7.0556 * mm, 207.58 * mm, 155.22 * mm, 32.46 * mm, 5)
        canvas.roundRect(162.9856 * mm, 207.58 * mm, 45.86 * mm, 64.56 * mm, 5)
        # Marco Detalle
        canvas.roundRect(7.0556 * mm, 87.01 * mm, 201.79 * mm, 119.94 * mm, 5)
        # Marcos Pie
        canvas.roundRect(7.0556 * mm, 69.02 * mm, 144.64 * mm, 16.93 * mm, 5)
        canvas.roundRect(152.3256 * mm, 69.02 * mm, 56.44 * mm, 16.93 * mm, 5)
        canvas.roundRect(7.0556 * mm, 13.99 * mm, 201.79 * mm, 54.50 * mm, 5)
        canvas.line(7.0556 * mm, 13.10 * mm, 208.8456 * mm, 13.10 * mm)
        return canvas

    def _set_lineas(self, canvas):
        # Líneas Grises punteadas
        canvas.setStrokeColorRGB(.80, .80, .80)  # Gris Claro
        canvas.setDash([0.5 * mm, 0.5 * mm], 0)
        # Líneas Grises punteadas Cabecera
        canvas.line(7.0556 * mm, 233.86 * mm, 162.2756 * mm, 233.86 * mm)
        canvas.line(135.9956 * mm, 240.04 * mm, 135.9956 * mm, 233.86 * mm)
        canvas.line(147.2856 * mm, 240.04 * mm, 147.2856 * mm, 233.86 * mm)
        y_factura = 212.34 * mm
        canvas.line(162.9856 * mm, y_factura, 208.8456 * mm, y_factura)
        for _ in range(12):
            y_factura += 4.59 * mm
            canvas.line(162.9856 * mm, y_factura, 208.8456 * mm, y_factura)
        # Líneas Grises punteadas Detalle
        canvas.line(7.0556 * mm, 199.37 * mm, 208.8456 * mm, 199.37 * mm)
        return canvas

    def _config_pie(self):
        self._frame_pie_datos = Frame(
            7.0556 * mm,
            69.02 * mm,
            width=144.64 * mm,
            height=16.93 * mm,
            id="PieDatos",
            leftPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self._frame_pie_totales = Frame(
            152.3256 * mm,
            69.02 * mm,
            width=56.44 * mm,
            height=16.93 * mm,
            id='PieTotales',
            leftPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self._frame_pie_info = Frame(
            38.3256 * mm,
            13.99 * mm,
            width=170.52 * mm,
            height=54.50 * mm,
            id='PieInfo',
            leftPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self._flowables_pie_datos = []
        self._flowables_pie_totales = []
        self._flowables_pie_info = []
        tabla_pie = Table(
            self._info_extra,
            colWidths=[
                25.41 * mm,
                48.99 * mm,
                28.60 * mm,
                25 * mm,
            ]
        )
        tabla_pie.setStyle(self._estilo_tabla_info)
        tabla_pie.vAlign = 'TOP'
        tabla_pie.hAlign = 'LEFT'
        self._flowables_pie_datos.append(tabla_pie)

        tabla_totales = Table(
            self._info_totales,
            colWidths=[32.59 * mm, 23.85 * mm]
        )
        tabla_totales.setStyle(self._estilo_tabla_totales)
        tabla_totales.vAlign = 'TOP'
        tabla_totales.hAlign = 'LEFT'
        self._flowables_pie_totales.append(tabla_totales)

        info_info = [
            ['Sello digital del CFDI:'],
            [Paragraph(self._comprobante.timbre.sello_cfd, self._small)],
            ['Sello del SAT:'],
            [Paragraph(self._comprobante.timbre.sello_sat, self._small)],
            [('Cadena original del complemento de certificación digital del '
              'SAT:')],
            [Paragraph(self._comprobante.timbre.cadena_original, self._small)],
        ]
        tabla_info = Table(
            info_info,
            colWidths=170.52 * mm,
        )
        tabla_info.setStyle(self._estilo_tabla_info_qr)
        self._flowables_pie_info.append(tabla_info)

    def _config_cabecera(self, canvas):
        emisor = self._comprobante.emisor
        receptor = self._comprobante.receptor
        if self._archivo_logo != '':
            ruta_logo = os.sep.join(self._ruta_logos) + os.sep + self._archivo_logo
            canvas.drawImage(
                ruta_logo,
                7.0556 * mm,
                240.50 * mm,
                width=36.49 * mm,
                height=32.10 * mm
            )
        datos_emisor = f'<b>{emisor.nombre}</b><br/><para leading=8>'

        datos_emisor += (f'<font size=8>{emisor.calle_numero}<br/>'
                         + f'COL. {emisor.colonia}<br/>'
                         + f'{emisor.ciudad}<br/>{emisor.estado_pais}<br/>'
                         + f'C.P. {emisor.codigo_postal}<br/>'
                         + f'R.F.C. {emisor.rfc}<br/>'
                         + f'Regímen fiscal: {emisor.regimen_fiscal}</font>')

        titulos_receptor = [[
            'Receptor del comprobante', 'Clave:',
            self._comprobante.receptor.clave,
        ]]
        datos_receptor = (f'<font size=8>{receptor.nombre}</font><br/><br/>'
                          + f'{receptor.calle}<br/>'
                          + f'COL. {receptor.colonia}<br/>'
                          + f'{receptor.municipio}<br/>'
                          + f'{receptor.estado}, {receptor.pais}<br/>'
                          + f'C.P. {receptor.codigo_postal}<br/>'
                          + f'R.F.C. {receptor.rfc}<br/>')

        serie_folio = f'{self._comprobante.serie}-{self._comprobante.folio}'
        fecha_emision = self._comprobante.fecha
        serie_cert_emisor = self._comprobante.no_certificado
        uuid = self._comprobante.timbre.uuid
        serie_cert_sat = self._comprobante.timbre.no_certificado_sat
        fecha_hora_cert = self._comprobante.timbre.fecha_timbrado
        lugar_expedicion = self._comprobante.lugar_expedicion

        titulo_comprobante = self.genera_titulos()
        titulos_documento = [
            [titulo_comprobante],
            [serie_folio],
            ['Fecha de emisión del CFDI'],
            [fecha_emision],
            ['No. serie certificado emisor'],
            [serie_cert_emisor],
            ['Folio fiscal'],
            [uuid],
            ['No. serie certificado SAT'],
            [serie_cert_sat],
            ['Fecha y hora de certificación'],
            [fecha_hora_cert],
            ['Lugar expedición'],
            [lugar_expedicion],
        ]

        para_emisor = Paragraph(datos_emisor, self._styles['Normal'])
        para_emisor.wrapOn(canvas, 106 * mm, 31 * mm)
        para_emisor.drawOn(canvas, 49.55 * mm, 247 * mm)
        titulos = Table(
            titulos_receptor,
            colWidths=[
                128.94 * mm, 11.29 * mm, 15.522 * mm
            ],
        )
        titulos.setStyle(self._estilo_tabla_titulos)
        titulos.wrapOn(canvas, 0, 0)
        titulos.drawOn(canvas, 6 * mm, 233.86 * mm)
        tabla_documento = Table(
            titulos_documento,
            colWidths=45.86 * mm,
            rowHeights=4.61 * mm,
        )
        tabla_documento.setStyle(self._estilo_tabla_doc)
        tabla_documento.wrapOn(canvas, 0, 0)
        tabla_documento.drawOn(canvas, 162.9856 * mm, 207.58 * mm)
        para_receptor = Paragraph(datos_receptor, self._small)
        para_receptor.wrapOn(canvas, 155.22 * mm, 26.28 * mm)
        para_receptor.drawOn(canvas, 7.5 * mm, 212.58 * mm)
        return canvas

    def _set_qr(self):
        qr_code = qr.QrCodeWidget(
            f'?re={self._comprobante.emisor.rfc}'
            + f'&rr={self._comprobante.receptor.rfc}'
            + f'&tt={self._comprobante.total}&id='
            + f'{self._comprobante.timbre.uuid}'
        )
        qr_code.barWidth = 30 * mm
        qr_code.barHeight = 30 * mm
        qr_code.qrVersion = 1
        d = Drawing()
        d.add(qr_code)
        return d

    def _primera_hoja(self, canvas, document):
        canvas = self._propiedades_canvas(canvas)
        self._set_tamanos()
        self._set_estilos()
        self._datos_pie()
        self._config_pie()

        canvas.saveState()
        canvas = self._set_marcos(canvas)
        canvas = self._config_cabecera(canvas)

        # Pie
        self._frame_pie_datos.addFromList(self._flowables_pie_datos, canvas)
        self._frame_pie_totales.addFromList(self._flowables_pie_totales,
                                            canvas)
        self._frame_pie_info.addFromList(self._flowables_pie_info, canvas)

        canvas.setFont('Helvetica-Bold', 14)
        canvas.drawString(
            36.955 * mm,
            7.83 * mm,
            'Este documento es una representación impresa de un CFDI.'
        )

        renderPDF.draw(self._set_qr(), canvas, 8 * mm, 37 * mm)
        canvas = self._set_lineas(canvas)
        canvas.restoreState()

    def _propiedades_documento(self):
        doc = SimpleDocTemplate(
            self.nombre,
            pagesize=letter,
            rightMargin=7.0556 * mm,
            leftMargin=7.0556 * mm,
            topMargin=72.55 * mm,
            bottomMargin=86.79 * mm,
        )
        return doc

    def _define_layout(self):
        documento = self._propiedades_documento()
        flowables = []
        lista_detalle = [
            [
                'Cantidad',
                'Unidad',
                'Clave',
                'Descripción',
                'Precio',
                'Importe',
            ],
        ]
        for concepto in self._comprobante.conceptos:
            fila = [
                concepto.cantidad,
                concepto.clave_unidad,
                concepto.clave_prod_serv,
                Paragraph(concepto.descripcion, self._styles['Normal']),
                f'${float(concepto.valor_unitario):,.2f}',
                f'${float(concepto.importe):,.2f}',
            ]
            lista_detalle.append(fila)
        # Detalle
        tabla_detalle = Table(
            lista_detalle,
            colWidths=[
                26.65 * mm,
                24.33 * mm,
                23.98 * mm,
                71.93 * mm,
                29.91 * mm,
                24.40 * mm,
            ],
            repeatRows=1,
        )
        estilo_tabla_detalle = TableStyle([
            ('SIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ])
        tabla_detalle.setStyle(estilo_tabla_detalle)
        t = tabla_detalle.split(201.79 * mm, 119.94 * mm)
        for x in t:
            flowables.append(x)

        documento.build(flowables, onFirstPage=self._primera_hoja,
                        onLaterPages=self._primera_hoja)

    def resuelve_codigos(self):
        try:
            with open('catalogos.db', encoding='utf-8') as catalogo:
                for linea in catalogo:
                    linea = linea.strip()
                    if linea.startswith('[') and linea.endswith(']'):
                        titulo = linea[1:-1]
                    elif '=' in linea:
                        clave, des = linea.split('=')
                        if (
                            titulo == 'FormasPago' and
                            self._comprobante.forma_pago == clave
                        ):
                            self._comprobante.forma_pago += f' {des}'
                        if (
                            titulo == 'UsosCFDI' and
                            self._comprobante.receptor.uso_cfdi == clave
                        ):
                            self._comprobante.receptor.uso_cfdi += f' {des}'
                        if (
                            titulo == 'MetodosPago'
                            and self._comprobante.metodo_pago == clave
                        ):
                            self._comprobante.metodo_pago += f' {des}'

        except FileNotFoundError as fnfe:
            print(fnfe)

    def genera_titulos(self):
        genero = self._comprobante.nombre_archivo[3]
        naturaleza = self._comprobante.nombre_archivo[4]
        grupo = self._comprobante.nombre_archivo[5:7]

        if self._comprobante.tipo_comprobante == 'P':
            return 'PAGO'
        if self._comprobante.tipo_comprobante == 'E':
            return 'NOTA DE CRÉDITO'
        if self._comprobante.tipo_comprobante == 'I':
            if genero == 'U' and naturaleza == 'D' and grupo == '03':
                return 'NOTA DE CARGO'

            return 'FACTURA'

        return 'SIN DEFINIR'

    def genera_pdf(self):
        self._lee_ini()
        self._define_layout()


class ImpresionServicio(ImpresionComprobante):
    def __init__(self, comprobante):
        super().__init__(comprobante)

    def _set_marcos(self, canvas):
        rojo, verde, azul = self._codigo_color_lineas[1:-1].split(',')
        canvas.setStrokeColorRGB(float(rojo), float(verde), float(azul))
        # Marcos Cabecera
        canvas.roundRect(7.0556 * mm, 207.58 * mm, 155.22 * mm, 32.46 * mm, 5)
        canvas.roundRect(162.9856 * mm, 207.58 * mm, 45.86 * mm, 64.56 * mm, 5)
        canvas.roundRect(7.0556 * mm, 168.04 * mm, 201.79 * mm, 38.81 * mm, 5)
        # Marco Detalle
        canvas.roundRect(7.0556 * mm, 87.01 * mm, 201.79 * mm, 80.3 * mm, 5)
        # Marcos Pie
        canvas.roundRect(7.0556 * mm, 69.02 * mm, 144.64 * mm, 16.93 * mm, 5)
        canvas.roundRect(152.3256 * mm, 69.02 * mm, 56.44 * mm, 16.93 * mm, 5)
        canvas.roundRect(7.0556 * mm, 13.99 * mm, 201.79 * mm, 54.50 * mm, 5)
        canvas.line(7.0556 * mm, 13.10 * mm, 208.8456 * mm, 13.10 * mm)
        return canvas

    def _set_lineas(self, canvas):
        # Líneas Grises punteadas
        canvas.setStrokeColorRGB(.80, .80, .80)  # Gris Claro
        canvas.setDash([0.5 * mm, 0.5 * mm], 0)
        # Líneas Grises punteadas Cabecera
        canvas.line(7.0556 * mm, 233.86 * mm, 162.2756 * mm, 233.86 * mm)
        canvas.line(135.9956 * mm, 240.04 * mm, 135.9956 * mm, 233.86 * mm)
        canvas.line(147.2856 * mm, 240.04 * mm, 147.2856 * mm, 233.86 * mm)
        y_factura = 212.34 * mm
        canvas.line(162.9856 * mm, y_factura, 208.8456 * mm, y_factura)
        for _ in range(12):
            y_factura += 4.59 * mm
            canvas.line(162.9856 * mm, y_factura, 208.8456 * mm, y_factura)
        # Líneas Grises punteadas Detalle
        canvas.line(7.0556 * mm, 160 * mm, 208.8456 * mm, 160 * mm)
        return canvas

    def _propiedades_documento(self):
        doc = SimpleDocTemplate(
            self.nombre,
            pagesize=letter,
            rightMargin=7.0556 * mm,
            leftMargin=7.0556 * mm,
            topMargin=111.57 * mm,
            bottomMargin=86.79 * mm,
        )
        return doc

    def _segunda_cabecera(self, canvas):
        veh = self._comprobante.vehiculo
        info_seg_cab = [
            ['Marca', 'Tipo Modelo', 'Año', 'Color', 'Número de serie'],
            [veh.marca, veh.modelo, veh.anio, veh.color, veh.serie],
            ['Kilometraje', 'Placas', 'Motor', 'Bonete', 'Referencia'],
            [veh.kilometraje, veh.placas, veh.motor,
             veh.bonete, veh.referencia],
            ['Recepcionista', '', '', '', 'Siniestro/O. Compra'],
            [veh.recepcionista, '', '', '', veh.siniestro],
        ]
        tabla_segunda = Table(
            info_seg_cab,
            colWidths=[
                40.358 * mm,
                40.358 * mm,
                40.358 * mm,
                40.358 * mm,
                40.358 * mm,
            ]
        )
        tabla_segunda.setStyle(self._estilo_seg_cab)
        tabla_segunda.wrapOn(canvas, 0, 0)
        tabla_segunda.drawOn(canvas, 7 * mm, 175 * mm)
        return canvas

    def _primera_hoja(self, canvas, document):
        canvas = self._propiedades_canvas(canvas)
        self._set_tamanos()
        self._set_estilos()
        self._datos_pie()
        self._config_pie()

        canvas.saveState()
        canvas = self._set_marcos(canvas)
        canvas = self._config_cabecera(canvas)
        canvas = self._segunda_cabecera(canvas)

        # Pie
        self._frame_pie_datos.addFromList(self._flowables_pie_datos, canvas)
        self._frame_pie_totales.addFromList(self._flowables_pie_totales,
                                            canvas)
        self._frame_pie_info.addFromList(self._flowables_pie_info, canvas)

        canvas.setFont('Helvetica-Bold', 14)
        canvas.drawString(
            36.955 * mm,
            7.83 * mm,
            'Este documento es una representación impresa de un CFDI.'
        )

        renderPDF.draw(self._set_qr(), canvas, 8 * mm, 37 * mm)
        canvas = self._set_lineas(canvas)
        canvas.restoreState()

    def _define_layout(self):
        documento = self._propiedades_documento()
        flowables = []
        lista_detalle = [
            [
                'Cant',
                'Unidad',
                'Clave SAT',
                'Clave Interna',
                'Descripción',
                'Precio',
                'Importe',
            ],
        ]
        for concepto in self._comprobante.conceptos:
            fila = [
                concepto.cantidad,
                concepto.clave_unidad,
                concepto.clave_prod_serv,
                concepto.clave_interna,
                Paragraph(concepto.descripcion, self._styles['Normal']),
                f'${float(concepto.valor_unitario):,.2f}',
                f'${float(concepto.importe):,.2f}',
            ]
            lista_detalle.append(fila)
        # Detalle
        tabla_detalle = Table(
            lista_detalle,
            colWidths=[
                9.45 * mm,
                13.5 * mm,
                23.98 * mm,
                23.98 * mm,
                71.93 * mm,
                29.91 * mm,
                24.40 * mm,
            ],
            repeatRows=1,
        )
        estilo_tabla_detalle = TableStyle([
            ('SIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (5, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 1), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ])
        tabla_detalle.setStyle(estilo_tabla_detalle)
        t = tabla_detalle.split(201.79 * mm, 80.3 * mm)
        for x in t:
            flowables.append(x)

        documento.build(flowables, onFirstPage=self._primera_hoja,
                        onLaterPages=self._primera_hoja)


class ImpresionVehiculos(ImpresionServicio):
    def __init__(self, comprobante):
        super().__init__(comprobante)


class ImpresionPago(ImpresionComprobante):
    def _propiedades(self):
        self._autor = 'Enrique Santana Anaya'
        self._titulo = 'Representación impresa de un CFDI'
        self._pdf_titulo = 'Complemento de Pago'
        self._creador = 'ProLeCSA'

    def _datos_pie(self):
        self._info_extra = [
            [self._comprobante.total_letra, '', '', ''],
            [
                'Forma de pago:',
                self._comprobante.pagos[0].forma_pago_p,
                'Unidad de medida:',
                self._comprobante.conceptos[0].clave_unidad
            ],
            [
                'Uso de CFDI:',
                self._comprobante.receptor.uso_cfdi,
                'Clave de Producto:',
                self._comprobante.conceptos[0].clave_prod_serv
            ],
            ['Número de cuenta:', self._comprobante.cuenta_pago, '', ''],
        ]
        monto = float(self._comprobante.pagos[0].monto)
        self._info_totales = [
            ['Total:', f'${monto:,.2f}'],
        ]

    def __init__(self, comprobante):
        super().__init__(comprobante)

    def resuelve_codigos(self):
        try:
            with open('catalogos.db', encoding='utf-8') as catalogo:
                for linea in catalogo:
                    linea = linea.strip()
                    if linea.startswith('[') and linea.endswith(']'):
                        titulo = linea[1:-1]
                    elif '=' in linea:
                        clave, des = linea.split('=')
                        if (
                            titulo == 'FormasPago' and
                            self._comprobante.pagos[0].forma_pago_p == clave
                        ):
                            self._comprobante.pagos[0].forma_pago_p += f' {des}'
                        if (
                            titulo == 'UsosCFDI' and
                            self._comprobante.receptor.uso_cfdi == clave
                        ):
                            self._comprobante.receptor.uso_cfdi += f' {des}'
        except FileNotFoundError as fnfe:
            print(fnfe)

    def _define_layout(self):
        documento = self._propiedades_documento()
        flowables = []
        lista_detalle = [
            [
                'Pago correspondiente a: Folio Fiscal',
                'Folio y Serie',
                'Moneda',
                'Met. Pago',
                'N° Parc.',
                'Saldo Ant.',
                'Imp. Pagado',
                'Saldo Insoluto',
            ],
        ]
        for pago in self._comprobante.pagos:
            fila = [
                pago.docto_relacionado.id_documento,
                (pago.docto_relacionado.serie
                 + pago.docto_relacionado.folio),
                pago.docto_relacionado.moneda_dr,
                pago.docto_relacionado.metodo_pago_dr,
                pago.docto_relacionado.num_parcialidad,
                f'${float(pago.docto_relacionado.imp_saldo_ant):,.2f}',
                f'${float(pago.docto_relacionado.imp_pagado):,.2f}',
                f'${float(pago.docto_relacionado.imp_saldo_insoluto):,.2f}',
            ]
            lista_detalle.append(fila)
        # Detalle
        tabla_detalle = Table(
            lista_detalle,
            colWidths=[
                65.73 * mm,
                22.07 * mm,
                14.56 * mm,
                17.40 * mm,
                13.77 * mm,
                19.24 * mm,
                22.06 * mm,
                24.89 * mm,
            ],
            repeatRows=1,
        )
        estilo_tabla_detalle = TableStyle([
            ('SIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
        ])
        tabla_detalle.setStyle(estilo_tabla_detalle)
        t = tabla_detalle.split(201.79 * mm, 119.94 * mm)
        for x in t:
            flowables.append(x)

        documento.build(flowables, onFirstPage=self._primera_hoja,
                        onLaterPages=self._primera_hoja)
