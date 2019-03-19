import os

from lxml import etree as ET

from .legacy_db import get_conceptos, get_cab_comp, get_datos_vehiculo
from .comprobantePdf import (Comprobante, Concepto, DoctoRelacionado, Emisor,
                             Pago, Receptor, TimbreFiscalDigital, Vehiculo)


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


def cons_f33(comprobante):
    vehiculo = Vehiculo()
    conceptos = []
    datos_conceptos = get_conceptos(comprobante.emisor.rfc,
                                    comprobante.nombre_archivo[:-4])
    for reg in datos_conceptos:
        concepto = Concepto(reg[0], reg[3], reg[4], reg[1],
                            reg[5], str(reg[7]), str(reg[6]))
        conceptos.append(concepto)
    comprobante.conceptos = conceptos
    datos_cab = get_cab_comp(comprobante.emisor.rfc,
                             comprobante.nombre_archivo[:-4])
    datos_veh = get_datos_vehiculo(comprobante.emisor.rfc,
                                   comprobante.nombre_archivo[:-4])
    comprobante.total_letra = datos_cab[7]
    comprobante.cuenta_pago = datos_cab[8]
    vehiculo.marca = datos_veh[0]
    vehiculo.modelo = datos_veh[1]
    vehiculo.anio = datos_veh[2]
    vehiculo.color = datos_veh[3]
    vehiculo.serie = datos_veh[4]
    vehiculo.kilometraje = datos_veh[5]
    vehiculo.placas = datos_veh[6]
    vehiculo.motor = datos_veh[7]
    vehiculo.referencia = datos_veh[8]
    vehiculo.recepcionista = datos_veh[9]
    vehiculo.siniestro = datos_veh[10]
    vehiculo.bonete = datos_veh[11]
    comprobante.vehiculo = vehiculo
    return comprobante
