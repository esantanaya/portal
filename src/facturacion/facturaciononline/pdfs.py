import os
import re
import traceback

from lxml import etree as ET

from .layout import ImpresionComprobante, ImpresionPago, ImpresionServicio
from .comprobantePdf import (Comprobante, Concepto, DoctoRelacionado, Emisor, Pago,
                         Receptor, TimbreFiscalDigital, Vehiculo)


def construye_comprobante(tree, archivo):
    root = tree.getroot()

    ns_cfdi = '{http://www.sat.gob.mx/cfd/3}'
    ns_pago10 = '{http://www.sat.gob.mx/Pagos}'
    ns_tfd = '{http://www.sat.gob.mx/TimbreFiscalDigital}'
    element_pagos = None
    for child in root:
        if child.tag == f'{ns_cfdi}Emisor':
            emisor = Emisor(
                child.attrib['Nombre'],
                child.attrib['RegimenFiscal'],
                child.attrib['Rfc']
            )
        elif child.tag == f'{ns_cfdi}Receptor':
            receptor = Receptor(
                child.attrib['Nombre'],
                child.attrib['Rfc'],
                child.attrib['UsoCFDI'],
            )
        elif child.tag == f'{ns_cfdi}Complemento':
            for grandchild in child:
                if grandchild.tag == f'{ns_pago10}Pagos':
                    element_pagos = list(grandchild)
                if grandchild.tag == f'{ns_tfd}TimbreFiscalDigital':
                    str_timbre = ET.tostring(grandchild)
                    xdoc = ET.fromstring(str_timbre)
                    xslt = ET.parse(
                        os.path.join('facturaciononline', 'static',
                                     'recursos', 'xslt',
                                     'cadenaoriginal_TFD_1_1.xslt')
                    )
                    trans = ET.XSLT(xslt)
                    doc = trans(xdoc)
                    timbre = TimbreFiscalDigital(
                        grandchild.attrib['FechaTimbrado'],
                        grandchild.attrib['NoCertificadoSAT'],
                        grandchild.attrib['RfcProvCertif'],
                        grandchild.attrib['SelloCFD'],
                        grandchild.attrib['SelloSAT'],
                        grandchild.attrib['UUID'],
                        grandchild.attrib['Version'],
                        str(doc),
                    )

    pagos = []
    if element_pagos is not None:
        for element_pago in element_pagos:
            element_docto = element_pago.find(
                f'{ns_pago10}DoctoRelacionado')
            docto = DoctoRelacionado(
                element_docto.attrib['Folio'],
                element_docto.attrib['IdDocumento'],
                element_docto.attrib['ImpPagado'],
                element_docto.attrib['ImpSaldoAnt'],
                element_docto.attrib['ImpSaldoInsoluto'],
                element_docto.attrib['MetodoDePagoDR'],
                element_docto.attrib['MonedaDR'],
                element_docto.attrib['NumParcialidad'],
                element_docto.attrib['Serie'],
            )
            pago = Pago(
                element_pago.attrib['FechaPago'],
                element_pago.attrib['FormaDePagoP'],
                element_pago.attrib['MonedaP'],
                element_pago.attrib['Monto'],
                docto,
            )
            pagos.append(pago)

    if root.tag == f'{ns_cfdi}Comprobante':
        print(f'Creando comprobante')
        comprobante = Comprobante(
            archivo,
            root.attrib['NoCertificado'],
            root.attrib['Fecha'],
            root.attrib['Folio'],
            root.attrib['LugarExpedicion'],
            root.attrib['Moneda'],
            root.attrib['Sello'],
            root.attrib['Serie'],
            root.attrib['SubTotal'],
            root.attrib['TipoDeComprobante'],
            root.attrib['Total'],
            root.attrib['Version'],
            emisor,
            receptor,
            pagos=pagos,
            timbre=timbre,
        )

        if comprobante.tipo_comprobante != 'P':
            comprobante.forma_pago = root.attrib['FormaPago']
            comprobante.metodo_pago = root.attrib['MetodoPago']

    return comprobante


def cons_f33(comprobante, archivo_f33, mensaje=None):
    vehiculo = Vehiculo()
    conceptos = []
    try:
        with open(archivo_f33, 'r') as f33:
            if mensaje:
                print('Encontramos el F33 en errores!')
            for linea in f33:
                t_lin = linea.rstrip().split('|')
                if t_lin[0] == 'CONCEPTO':
                    concepto = Concepto(t_lin[1], t_lin[3], t_lin[11],
                                        t_lin[2], t_lin[4], t_lin[6],
                                        t_lin[5])
                    conceptos.append(concepto)
        with open(archivo_f33, 'r') as f33:
            lineas = {
                x.rstrip().split('|')[0]:
                x.rstrip().split('|')[1:] for x in f33
            }
        comprobante.conceptos = conceptos
        comprobante.total_letra = lineas['DOCUMENTO'][15]
        comprobante.cuenta_pago = lineas['DOCUMENTO'][13]
        comprobante.receptor.clave = lineas['CLIENTE'][0]
        comprobante.receptor.calle = lineas['CLIENTE'][2]
        comprobante.receptor.colonia = lineas['CLIENTE'][3]
        comprobante.receptor.municipio = lineas['CLIENTE'][10]
        comprobante.receptor.estado = lineas['CLIENTE'][11]
        comprobante.receptor.pais = lineas['CLIENTE'][12]
        comprobante.receptor.codigo_postal = lineas['CLIENTE'][7]
        vehiculo.marca = lineas['VEHICULO'][1]
        vehiculo.modelo = lineas['VEHICULO'][2]
        vehiculo.anio = lineas['VEHICULO'][3]
        vehiculo.color = lineas['VEHICULO'][4]
        vehiculo.serie = lineas['VEHICULO'][0]
        vehiculo.kilometraje = lineas['VEHICULO'][8]
        vehiculo.placas = lineas['VEHICULO'][9]
        vehiculo.motor = lineas['VEHICULO'][5]
        vehiculo.referencia = (f'{lineas["VEHICULO"][6]}-'
                               f'{lineas["VEHICULO"][7]}')
        vehiculo.recepcionista = lineas['VEHICULO'][10]
        vehiculo.siniestro = lineas['EXTRAS'][6]
        vehiculo.bonete = lineas['EXTRAS'][7]
    except IndexError:
        vehiculo.siniestro = 'NA'
        vehiculo.bonete = 'NA'
    except FileNotFoundError:
        raise FileNotFoundError
    finally:
        comprobante.vehiculo = vehiculo
    return comprobante


def compl_comp_f33(comprobante, archivo_f33):
    print(f'leyendo archivo {archivo_f33}')
    try:
        comprobante = cons_f33(comprobante, archivo_f33)
    except FileNotFoundError as ffe:
        print(f'{ffe} | Buscando en Errores!')
        archivo_error = archivo_f33.replace('Procesado', 'Errores')
        try:
            comprobante = cons_f33(comprobante, archivo_error, 1)
        except FileNotFoundError as e:
            print(f'{e} | tampoco lo encontramos en errores!')
            with open('errores.log', '+a') as log:
                log.write('\n'+str(e))
    finally:
        return comprobante
