import base64
import csv
import os
import re
import configparser
import logging
from datetime import datetime

from lxml import etree as et
from .chilkat import CkPrivateKey, CkRsa
from django.conf import settings
import requests

from .legacy_db import get_emisor


logging.basicConfig(filename=os.path.join(
                        'facturaciononline',
                        'static',
                        'logs',
                        'comprobante.log',
                    ),
                    format='%(asctime)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')


class Comprobante:
    def __init__(self, nombre_archivo, fecha, serie, folio, subtotal, total,
                 tipo_comprobante, version, emisor, receptor, forma_pago,
                 metodo_pago, total_letra, cuenta_pago, impuesto, moneda='MXN',
                 sello=None, lugar_expedicion=None, conceptos=None, pagos=None,
                 timbre=None, certificado=None, nro_certificado=None):
        self._nombre_archivo = f'{nombre_archivo}.xml'
        self._fecha = fecha
        self._serie = serie
        self._folio = folio
        self._subtotal = subtotal
        self._total = total
        self._tipo_comprobante = tipo_comprobante
        self._version = version
        self._emisor = emisor
        self._receptor = receptor
        self._forma_pago = forma_pago
        self._metodo_pago = metodo_pago
        self._total_letra = total_letra
        self._cuenta_pago = cuenta_pago
        self._impuesto = impuesto
        self._moneda = moneda
        self._sello = sello
        self._lugar_expedicion = lugar_expedicion
        self._conceptos = conceptos
        self._pagos = pagos
        self._timbre = timbre
        self._certificado = certificado
        self._nro_certificado = nro_certificado
        self._xmlns_cfdi = 'http://www.sat.gob.mx/cfd/3'
        self._xmlns_xsi = 'http://www.w3.org/2001/XMLSchema-instance'
        self._namespaces = {'cfdi': self._xmlns_cfdi, 'xsi': self._xmlns_xsi}
        self._schemaLocation = (
            'http://www.sat.gob.mx/cfd/3 http://www.sat.gob.mx/sitio_internet/'
            'cfd/3/cfdv33.xsd')

    @property
    def nombre_archivo(self):
        return self._nombre_archivo

    @nombre_archivo.setter
    def nombre_archivo(self, nombre_archivo):
        self._nombre_archivo = f'{nombre_archivo}.xml'

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, fecha):
        self._fecha = fecha

    @property
    def folio(self):
        return self._folio

    @folio.setter
    def folio(self, folio):
        self._folio = folio

    @property
    def lugar_expedicion(self):
        return self._lugar_expedicion

    @lugar_expedicion.setter
    def lugar_expedicion(self, lugar_expedicion):
        self._lugar_expedicion = lugar_expedicion

    @property
    def moneda(self):
        return self._moneda

    @moneda.setter
    def moneda(self, moneda):
        self._moneda = moneda

    @property
    def sello(self):
        return self._sello

    @sello.setter
    def sello(self, sello):
        self._sello = sello

    @property
    def serie(self):
        return self._serie

    @serie.setter
    def serie(self, serie):
        self._serie = serie

    @property
    def subtotal(self):
        return self._subtotal

    @subtotal.setter
    def subtotal(self, subtotal):
        self._subtotal = subtotal

    #TODO cambiar el diccionario tipos por una BD
    @property
    def tipo_comprobante(self):
        tipos = {
            'Ingreso': 'I',
            'Egreso': 'E',
            'Pago': 'P',
            'Traslado': 'T',
            'Nomina': 'N',
        }
        return tipos[self._tipo_comprobante.capitalize()]

    @tipo_comprobante.setter
    def tipo_comprobante(self, tipo_comprobante):
        self._tipo_comprobante = tipo_comprobante

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, total):
        self._total = total

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version

    @property
    def emisor(self):
        return self._emisor

    @emisor.setter
    def emisor(self, emisor):
        self._emisor = emisor

    @property
    def receptor(self):
        return self._receptor

    @receptor.setter
    def receptor(self, receptor):
        self._receptor = receptor

    @property
    def forma_pago(self):
        return self._forma_pago

    @forma_pago.setter
    def forma_pago(self, forma_pago):
        self._forma_pago = forma_pago

    @property
    def metodo_pago(self):
        return self._metodo_pago

    @metodo_pago.setter
    def metodo_pago(self, metodo_pago):
        self._metodo_pago = metodo_pago

    @property
    def conceptos(self):
        return self._conceptos

    @conceptos.setter
    def conceptos(self, conceptos):
        self._conceptos = conceptos

    @property
    def pagos(self):
        return self._pagos

    @pagos.setter
    def pagos(self, pagos):
        self._pagos = pagos

    @property
    def timbre    (self):
        return self._timbre

    @timbre.setter
    def timbre(self, timbre):
        self._timbre = timbre

    @property
    def total_letra(self):
        return self._total_letra

    @total_letra.setter
    def total_letra(self, total_letra):
        self._total_letra = total_letra

    @property
    def cuenta_pago(self):
        return self._cuenta_pago

    @cuenta_pago.setter
    def cuenta_pago(self, cuenta_pago):
        self._cuenta_pago = cuenta_pago

    @property
    def impuesto(self):
        return self._impuesto

    @impuesto.setter
    def impuesto(self, impuesto):
        self._impuesto = impuesto

    @property
    def certificado(self):
        return self._certificado

    @certificado.setter
    def certificado(self, certificado):
        self._certificado = certificado

    def crea_xml(self):
        nv = Utilidades.no_vacio
        sd = Utilidades.seis_decimales
        dd = Utilidades.dos_decimales
        #TODO Esto debe de ir en BD
        self._emisor.get_emisor()
        self._certificado = Certificado(self._emisor.nom_archivo_certificado,
                                        self._emisor.nro_certificado,
                                        r'\\192.168.24.10|e$|cfd|Certificados')
        self._lugar_expedicion = self._emisor.codigo_postal
        attr_schema = et.QName(self._xmlns_xsi, 'schemaLocation')
        elemento = et.Element(
            f'{{{self._xmlns_cfdi}}}Comprobante',
            nsmap=self._namespaces,
            attrib={
                attr_schema: self._schemaLocation,
                'Certificado': str(self._certificado),
                'Fecha': self._fecha,
                'Folio': str(self._folio),
                'FormaPago': self._forma_pago,
                'LugarExpedicion': self._lugar_expedicion,
                'MetodoPago': self._metodo_pago,
                'Moneda': self._moneda,
                'NoCertificado': self._certificado.numero,
                'Serie': self._serie,
                'SubTotal': dd(self._subtotal),
                'TipoDeComprobante': self.tipo_comprobante,
                'Total': dd(self._total),
                'Version': self._version,
            })
        #Emisor
        et.SubElement(
            elemento,
            f'{{{self._xmlns_cfdi}}}Emisor',
            nsmap=self._namespaces,
            attrib={
                'Nombre': self._emisor.nombre,
                'RegimenFiscal': self._emisor.regimen_fiscal,
                'Rfc': self._emisor.rfc,
            }
        )
        #Receptor
        et.SubElement(
            elemento,
            f'{{{self._xmlns_cfdi}}}Receptor',
            nsmap=self._namespaces,
            attrib={
                'Nombre': self._receptor.nombre,
                'Rfc': self._receptor.rfc,
                'UsoCFDI': self._receptor.uso_cfdi,
            }
        )
        #Conceptos
        el_conceptos = et.SubElement(
            elemento,
            f'{{{self._xmlns_cfdi}}}Conceptos',
            nsmap=self._namespaces,
        )
        for concepto in self._conceptos:
            el_concepto = et.SubElement(
                el_conceptos,
                f'{{{self._xmlns_cfdi}}}Concepto',
                nsmap=self._namespaces,
                attrib={
                    'Cantidad': dd(concepto.cantidad),
                    'ClaveProdServ': concepto.clave_prod_serv,
                    'ClaveUnidad': concepto.clave_unidad,
                    'Descripcion': nv(concepto.descripcion),
                    'Importe': dd(concepto.importe),
                    'ValorUnitario': dd(concepto.valor_unitario),
                }
            )
            el_impuestos = et.SubElement(
                el_concepto,
                f'{{{self._xmlns_cfdi}}}Impuestos',
                nsmap=self._namespaces,
            )
            el_traslados = et.SubElement(
                el_impuestos,
                f'{{{self._xmlns_cfdi}}}Traslados',
                nsmap=self._namespaces,
            )
            et.SubElement(
                el_traslados,
                f'{{{self._xmlns_cfdi}}}Traslado',
                nsmap=self._namespaces,
                attrib={
                    'Base': dd(concepto.base_impuesto),
                    'Importe': dd(concepto.importe_impuesto),
                    'Impuesto': concepto.tipo_impuesto,
                    'TasaOCuota': sd(concepto.tasa_cuota),
                    'TipoFactor': concepto.tipo_factor.capitalize(),
                }
            )
        el_impuestos = et.SubElement(
            elemento,
            f'{{{self._xmlns_cfdi}}}Impuestos',
            nsmap=self._namespaces,
            attrib={
                'TotalImpuestosTrasladados': dd(self._impuesto.total),
            }
        )
        el_traslados = et.SubElement(
            el_impuestos,
            f'{{{self._xmlns_cfdi}}}Traslados',
            nsmap=self._namespaces,
        )
        et.SubElement(
            el_traslados,
            f'{{{self._xmlns_cfdi}}}Traslado',
            nsmap=self._namespaces,
            attrib={
                'Importe': dd(self._impuesto.total),
                'TipoFactor': self._impuesto.tipo_factor.capitalize(),
                'TasaOCuota': sd(self._impuesto.tasa_cuota),
                'Impuesto': self._impuesto.impuesto,
            }
        )
        arbol = self.sella_xml(elemento)
        return arbol

    def sella_xml(self, xml):
        conf = Configuracion()
        ruta_llave = os.sep.join([conf.ruta('llave'),
                               self._emisor.nom_archivo_llave])
        pswd = self._emisor.pswd_archivo_llave
        p_key = CkPrivateKey()
        success = p_key.LoadPkcs8EncryptedFile(ruta_llave, pswd)
        if not success:
            raise CFDIError('No se pudo cargar la llave')
        key_xml = p_key.getXml()

        ruta_xslt = os.sep.join([conf.ruta('xslt'), 'cadenaoriginal_3_3.xslt'])
        xslt_root = et.parse(ruta_xslt)
        xslt = et.XSLT(xslt_root)
        trans = xslt(xml)
        cadena = str(trans)

        rsa = CkRsa()
        success = rsa.UnlockComponent('ESANTA.RS1112018_aaVYzQhpQbme')
        if not success:
            raise CFDIError('No se pudo desbloquear RSA')
        success = rsa.ImportPrivateKey(key_xml)
        if not success:
            raise CFDIError('No se pudo importar el xml dentro del RSA')
        rsa.put_EncodingMode('base64')
        rsa.put_LittleEndian(False)
        sello = rsa.signStringENC(cadena, 'sha256')

        xml.attrib['Sello'] = sello
        return et.ElementTree(xml)

    def timbra_xml(self):
        conf = Configuracion()
        data = {'email': conf.user, 'password': conf.pswd}
        auth = requests.post(conf.url_auth, json=data)
        if auth.status_code != 200:
            raise CFDIError('No se pudo obtener el token de autenticacion'
                            f' {auth.status_code}')
        else:
            token = auth.json().get('token')
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'token {token}'
            }
            xml = self.crea_xml()
            xml = et.tostring(xml)
            xml = base64.b64encode(xml)
            xml = xml.decode('utf-8')
            data = {
                'xml': xml
            }
            timbre = requests.post(conf.url_timbre, headers=headers, json=data)
            if timbre.status_code != 200:
                raise CFDIError('No se pudo timbrar el CFDI '
                                f'Códgio de error: {timbre.status_code} '
                                f'Mensaje: {timbre.json()["message"]}')
            else:
                cad_xml = timbre.json().get('data').get('cfdi').encode()
                elemento_xml = et.fromstring(cad_xml)
                archivo_xml = et.ElementTree(elemento_xml)
                mes_anio = datetime.now().strftime('%m%Y')
                try:
                    archivo_xml.write(
                        os.path.join(
                            'facturaciononline',
                            'static',
                            'facturas',
                            mes_anio,
                            self._nombre_archivo
                        ),
                        encoding='utf-8',
                        pretty_print=True,
                        standalone=True
                    )
                except FileNotFoundError:
                    try:
                        os.mkdir(os.path.join(
                            'facturaciononline',
                            'static',
                            'facturas',
                            mes_anio,
                        ))
                        archivo_xml.write(
                            os.path.join(
                                'facturaciononline',
                                'static',
                                'facturas',
                                mes_anio,
                                self._nombre_archivo
                            ),
                            encoding='utf-8',
                            pretty_print=True,
                            standalone=True
                        )
                    except Exception as e:
                        logging.error(e)


class Emisor:
    def __init__(self, rfc, nombre=None, regimen_fiscal=None, calle_numero=None,
                 colonia=None, ciudad=None, estado_pais=None, codigo_postal=None,
                 nro_certificado=None, nom_archivo_certificado=None,
                 nom_archivo_llave=None, pswd_archivo_llave=None):
        self._rfc = rfc
        self._nombre = nombre
        self._regimen_fiscal = regimen_fiscal
        self._calle_numero = calle_numero
        self._colonia = colonia
        self._ciudad = ciudad
        self._estado_pais = estado_pais
        self._codigo_postal = codigo_postal
        self._nro_certificado = nro_certificado
        self._nom_archivo_certificado = nom_archivo_certificado
        self._nom_archivo_llave = nom_archivo_llave
        self._pswd_archivo_llave = pswd_archivo_llave

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def regimen_fiscal(self):
        return self._regimen_fiscal

    @regimen_fiscal.setter
    def regimen_fiscal(self, regimen_fiscal):
        self._regimen_fiscal = regimen_fiscal

    @property
    def rfc(self):
        return self._rfc

    @rfc.setter
    def rfc(self, rfc):
        self._rfc = rfc

    @property
    def calle_numero(self):
        return self._calle_numero

    @calle_numero.setter
    def calle_numero(self, calle_numero):
        self._calle_numero = calle_numero

    @property
    def colonia(self):
        return self._colonia

    @colonia.setter
    def colonia(self, colonia):
        self._colonia = colonia

    @property
    def ciudad(self):
        return self._ciudad

    @ciudad.setter
    def ciudad(self, ciudad):
        self._ciudad = ciudad

    @property
    def estado_pais(self):
        return self._estado_pais

    @estado_pais.setter
    def estado_pais(self, estado_pais):
        self._estado_pais = estado_pais

    @property
    def codigo_postal(self):
        return self._codigo_postal

    @codigo_postal.setter
    def codigo_postal(self, codigo_postal):
        self._codigo_postal = codigo_postal

    @property
    def nro_certificado(self):
        return self._nro_certificado

    @nro_certificado.setter
    def nro_certificado(self, nro_certificado):
        self._nro_certificado = nro_certificado

    @property
    def nom_archivo_certificado(self):
        return self._nom_archivo_certificado

    @nom_archivo_certificado.setter
    def nom_archivo_certificado(self, nom_archivo_certificado):
        self._nom_archivo_certificado = nom_archivo_certificado

    @property
    def nom_archivo_llave(self):
        return self._nom_archivo_llave

    @nom_archivo_llave.setter
    def nom_archivo_llave(self, nom_archivo_llave):
        self._nom_archivo_llave = nom_archivo_llave

    @property
    def pswd_archivo_llave(self):
        return self._pswd_archivo_llave

    @pswd_archivo_llave.setter
    def pswd_archivo_llave(self, pswd_archivo_llave):
        self._pswd_archivo_llave = pswd_archivo_llave

    def get_emisor(self):
        tit = {'rfc': 0, 'nombre': 1, 'calle': 2, 'numero_exterior': 3,
               'numero_interior': 4, 'colonia': 5, 'municipio': 6,
               'estado': 7, 'pais': 8, 'codigo_postal': 9,
               'regimen_fiscal': 10, 'numero_certificado': 11,
               'nombre_archivo_certificado': 12, 'nombre_archivo_llave': 13,
               'pswd_archivo_llave': 14}
        emisor_data = get_emisor(self._rfc)
        self._nombre = emisor_data[tit['nombre']]
        self._regimen_fiscal = emisor_data[tit['regimen_fiscal']]
        self._calle_numero = emisor_data[tit['calle']]
        self._colonia = emisor_data[tit['colonia']]
        self._ciudad = emisor_data[tit['municipio']]
        self._estado_pais = (emisor_data[tit['estado']]
                             + emisor_data[tit['pais']])
        self._codigo_postal = emisor_data[tit['codigo_postal']]
        self._nro_certificado = emisor_data[tit['numero_certificado']]
        self._nom_archivo_certificado = emisor_data[
            tit['nombre_archivo_certificado']
        ]
        self._nom_archivo_llave = emisor_data[tit['nombre_archivo_llave']]
        self._pswd_archivo_llave = emisor_data[tit['pswd_archivo_llave']]


class Receptor:
    def __init__(self, nombre, rfc, uso_cfdi, clave=None, calle=None,
                 colonia=None, municipio=None, estado=None, pais=None,
                 codigo_postal=None):
        self._nombre = nombre
        self._rfc = rfc
        self._uso_cfdi = uso_cfdi
        self._clave = clave
        self._calle = calle
        self._colonia = colonia
        self._municipio = municipio
        self._estado = estado
        self._pais = pais
        self._codigo_postal = codigo_postal

    @property
    def clave(self):
        return self._clave

    @clave.setter
    def clave(self, clave):
        self._clave = clave

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def rfc(self):
        return self._rfc

    @rfc.setter
    def rfc(self, rfc):
        self._rfc = rfc

    @property
    def uso_cfdi(self):
        return self._uso_cfdi

    @uso_cfdi.setter
    def uso_cfdi(self, uso_cfdi):
        self._uso_cfdi = uso_cfdi

    @property
    def calle(self):
        return self._calle

    @calle.setter
    def calle(self, calle):
        self._calle = calle

    @property
    def colonia(self):
        return self._colonia

    @colonia.setter
    def colonia(self, colonia):
        self._colonia = colonia

    @property
    def municipio(self):
        return self._municipio

    @municipio.setter
    def municipio(self, municipio):
        self._municipio = municipio

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, estado):
        self._estado = estado

    @property
    def pais(self):
        return self._pais

    @pais.setter
    def pais(self, pais):
        self._pais = pais

    @property
    def codigo_postal(self):
        return self._codigo_postal

    @codigo_postal.setter
    def codigo_postal(self, codigo_postal):
        self._codigo_postal = codigo_postal


class Concepto:
    def __init__(self, cantidad, clave_prod_serv, clave_unidad, descripcion,
                 importe, valor_unitario, tipo_impuesto, tasa_cuota,
                 importe_impuesto, base_impuesto, tipo_factor):
        self._cantidad = cantidad
        self._clave_prod_serv = clave_prod_serv
        self._clave_unidad = clave_unidad
        self._descripcion = descripcion
        self._importe = importe
        self._valor_unitario = valor_unitario
        self._tipo_impuesto = tipo_impuesto
        self._tasa_cuota = tasa_cuota
        self._importe_impuesto = importe_impuesto
        self._base_impuesto = base_impuesto
        self._tipo_factor = tipo_factor

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, cantidad):
        self._cantidad = cantidad

    @property
    def clave_prod_serv(self):
        if self._clave_prod_serv == '':
            self._clave_prod_serv = '01010101'
        return self._clave_prod_serv

    @clave_prod_serv.setter
    def clave_prod_serv(self, clave_prod_serv):
        self._clave_prod_serv = clave_prod_serv

    @property
    def clave_unidad(self):
        #Reemplazos comunes de clave en kepler
        reem_com = {
            'PZA': 'H87',
            'PIE': 'H87',
            'LT': 'LTR',
            '': 'C62',
        }
        if self._clave_unidad in reem_com:
            self._clave_unidad = reem_com.get(self._clave_unidad)
        return self._clave_unidad

    @clave_unidad.setter
    def clave_unidad(self, clave_unidad):
        self._clave_unidad = clave_unidad

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self._descripcion = descripcion

    @property
    def importe(self):
        return self._importe

    @importe.setter
    def importe(self, importe):
        self._importe = importe

    @property
    def valor_unitario(self):
        return self._valor_unitario

    @valor_unitario.setter
    def valor_unitario(self, valor_unitario):
        self._valor_unitario = valor_unitario

    @property
    def tipo_impuesto(self):
        return self._tipo_impuesto

    @tipo_impuesto.setter
    def tipo_impuesto(self, tipo_impuesto):
        self._tipo_impuesto = tipo_impuesto

    @property
    def tasa_cuota(self):
        return self._tasa_cuota

    @tasa_cuota.setter
    def tasa_cuota(self, tasa_cuota):
        self._tasa_cuota = tasa_cuota

    @property
    def importe_impuesto(self):
        return self._importe_impuesto

    @importe_impuesto.setter
    def importe_impuesto(self, importe_impuesto):
        self._importe_impuesto = importe_impuesto

    @property
    def base_impuesto(self):
        return self._base_impuesto

    @base_impuesto.setter
    def base_impuesto(self, base_impuesto):
        self._base_impuesto = base_impuesto

    @property
    def tipo_factor(self):
        return self._tipo_factor

    @tipo_factor.setter
    def tipo_factor(self, tipo_factor):
        self._tipo_factor = tipo_factor


class Impuestos:
    def __init__(self, total, impuesto, tasa_cuota, tipo_factor):
        self._total = total
        self._impuesto = impuesto
        self._tasa_cuota = tasa_cuota
        self._tipo_factor = tipo_factor

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, total):
        self._total = total

    @property
    def impuesto(self):
        return self._impuesto

    @impuesto.setter
    def impuesto(self, impuesto):
        self._impuesto = impuesto

    @property
    def tasa_cuota(self):
        return self._tasa_cuota

    @tasa_cuota.setter
    def tasa_cuota(self, tasa_cuota):
        self._tasa_cuota = tasa_cuota

    @property
    def tipo_factor(self):
        return self._tipo_factor

    @tipo_factor.setter
    def tipo_factor(self, tipo_factor):
        self._tipo_factor = tipo_factor


class DoctoRelacionado:
    def __init__(
        self,
        folio,
        id_documento,
        imp_pagado,
        imp_saldo_ant,
        imp_saldo_insoluto,
        metodo_pago_dr,
        moneda_dr,
        num_parcialidad,
        serie
    ):
        self._folio = folio
        self._id_documento = id_documento
        self._imp_pagado = imp_pagado
        self._imp_saldo_ant = imp_saldo_ant
        self._imp_saldo_insoluto = imp_saldo_insoluto
        self._metodo_pago_dr = metodo_pago_dr
        self._moneda_dr = moneda_dr
        self._num_parcialidad = num_parcialidad
        self._serie = serie

    @property
    def folio(self):
        return self._folio

    @folio.setter
    def folio(self, folio):
        self._folio = folio

    @property
    def id_documento(self):
        return self._id_documento

    @id_documento.setter
    def id_documento(self, id_documento):
        self._id_documento = id_documento

    @property
    def imp_pagado(self):
        return self._imp_pagado

    @imp_pagado.setter
    def imp_pagado(self, imp_pagado):
        self._imp_pagado = imp_pagado

    @property
    def imp_saldo_ant(self):
        return self._imp_saldo_ant

    @imp_saldo_ant.setter
    def imp_saldo_ant(self, imp_saldo_ant):
        self._imp_saldo_ant = imp_saldo_ant

    @property
    def imp_saldo_insoluto(self):
        return self._imp_saldo_insoluto

    @imp_saldo_insoluto.setter
    def imp_saldo_insoluto(self, imp_saldo_insoluto):
        self._imp_saldo_insoluto = imp_saldo_insoluto

    @property
    def metodo_pago_dr(self):
        return self._metodo_pago_dr

    @metodo_pago_dr.setter
    def metodo_pago_dr(self, metodo_pago_dr):
        self._metodo_pago_dr = metodo_pago_dr

    @property
    def moneda_dr(self):
        return self._moneda_dr

    @moneda_dr.setter
    def moneda_dr(self, moneda_dr):
        self._moneda_dr = moneda_dr

    @property
    def num_parcialidad(self):
        return self._num_parcialidad

    @num_parcialidad.setter
    def num_parcialidad(self, num_parcialidad):
        self._num_parcialidad = num_parcialidad

    @property
    def serie(self):
        return self._serie

    @serie.setter
    def serie(self, serie):
        self._serie = serie


class Pago:
    def __init__(
        self,
        fecha_pago,
        forma_pago_p,
        moneda,
        monto,
        docto_relacionado
    ):

        self._fecha_pago = fecha_pago
        self._forma_pago_p = forma_pago_p
        self._moneda = moneda
        self._monto = monto
        self._docto_relacionado = docto_relacionado

    @property
    def fecha_pago(self):
        return self._fecha_pago

    @fecha_pago.setter
    def fecha_pago(self, fecha_pago):
        self._fecha_pago = fecha_pago

    @property
    def forma_pago_p(self):
        return self._forma_pago_p

    @forma_pago_p.setter
    def forma_pago_p(self, forma_pago_p):
        self._forma_pago_p = forma_pago_p

    @property
    def moneda(self):
        return self._moneda

    @moneda.setter
    def moneda(self, moneda):
        self._moneda = moneda

    @property
    def monto(self):
        return self._monto

    @monto.setter
    def monto(self, monto):
        self._monto = monto

    @property
    def docto_relacionado(self):
        return self._docto_relacionado

    @docto_relacionado.setter
    def docto_relacionado(self, docto_relacionado):
        self._docto_relacionado = docto_relacionado


class TimbreFiscalDigital:
    def __init__(
        self,
        fecha_timbrado,
        no_certificado_sat,
        rfc_prov_certif,
        sello_cfd,
        sello_sat,
        uuid,
        version,
        cadena_original=None,
    ):

        self._fecha_timbrado = fecha_timbrado
        self._no_certificado_sat = no_certificado_sat
        self._rfc_prov_certif = rfc_prov_certif
        self._sello_cfd = sello_cfd
        self._sello_sat = sello_sat
        self._uuid = uuid
        self._version = version
        self._cadena_original = cadena_original

    @property
    def fecha_timbrado(self):
        return self._fecha_timbrado

    @fecha_timbrado.setter
    def fecha_timbrado(self, fecha_timbrado):
        self._fecha_timbrado = fecha_timbrado

    @property
    def no_certificado_sat(self):
        return self._no_certificado_sat

    @no_certificado_sat.setter
    def no_certificado_sat(self, no_certificado_sat):
        self._no_certificado_sat = no_certificado_sat

    @property
    def rfc_prov_certif(self):
        return self._rfc_prov_certif

    @rfc_prov_certif.setter
    def rfc_prov_certif(self, rfc_prov_certif):
        self._rfc_prov_certif = rfc_prov_certif

    @property
    def sello_cfd(self):
        return self._sello_cfd

    @sello_cfd.setter
    def sello_cfd(self, sello_cfd):
        self._sello_cfd = sello_cfd

    @property
    def sello_sat(self):
        return self._sello_sat

    @sello_sat.setter
    def sello_sat(self, sello_sat):
        self._sello_sat = sello_sat

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        self._uuid = uuid

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version

    @property
    def cadena_original(self):
        return self._cadena_original

    @cadena_original.setter
    def cadena_original(self, cadena_original):
        self._cadena_original = cadena_original


class Linea:
    def __init__(
        self,
        rfc=None,
        razon_social=None,
        calle_numero=None,
        colonia=None,
        ciudad=None,
        estado_pais=None,
        codigo_postal=None,
        regimen_fiscal=None,
        color=None,
        logo=None,
    ):
        self._rfc = rfc
        self._razon_social = razon_social
        self._calle_numero = calle_numero
        self._colonia = colonia
        self._ciudad = ciudad
        self._estado_pais = estado_pais
        self._codigo_postal = codigo_postal
        self._regimen_fiscal = regimen_fiscal
        self._color = color
        self._logo = logo

    @property
    def rfc(self):
        return self._rfc

    @rfc.setter
    def rfc(self, rfc):
        self._rfc = rfc

    @property
    def razon_social(self):
        return self._razon_social

    @razon_social.setter
    def razon_social(self, razon_social):
        self._razon_social = razon_social

    @property
    def calle_numero(self):
        return self._calle_numero

    @calle_numero.setter
    def calle_numero(self, calle_numero):
        self._calle_numero = calle_numero

    @property
    def colonia(self):
        return self._colonia

    @colonia.setter
    def colonia(self, colonia):
        self._colonia = colonia

    @property
    def ciudad(self):
        return self._ciudad

    @ciudad.setter
    def ciudad(self, ciudad):
        self._ciudad = ciudad

    @property
    def estado_pais(self):
        return self._estado_pais

    @estado_pais.setter
    def estado_pais(self, estado_pais):
        self._estado_pais = estado_pais

    @property
    def codigo_postal(self):
        return self._codigo_postal

    @codigo_postal.setter
    def codigo_postal(self, codigo_postal):
        self._codigo_postal = codigo_postal

    @property
    def regimen_fiscal(self):
        return self._regimen_fiscal

    @regimen_fiscal.setter
    def regimen_fiscal(self, regimen_fiscal):
        self._regimen_fiscal = regimen_fiscal

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def logo(self):
        return self._logo

    @logo.setter
    def logo(self, logo):
        self._logo = logo


class NombreComprobante:
    def __init__(self, nombre_completo):
        self._nombre_completo = nombre_completo
        self._serie = ''
        self._folio = 0

    @property
    def serie(self):
        try:
            self._serie = re.findall(r'[A-Z]+', self._nombre_completo)[0]
        except:
            pass

        return self._serie

    @property
    def folio(self):
        try:
            self._folio = re.findall(r'\d+', self._nombre_completo)[0]
        except:
            pass

        return self._folio


class Certificado:
    """
    Recibe la ruta de un certificado y es representado en forma de base64
    """
    def __init__(self, archivo, numero, ruta='utils|certificados'):
        self._numero = numero
        self._archivo = archivo
        self._ruta = ruta

    @property
    def ruta(self):
        return self._ruta

    @ruta.setter
    def ruta(self, ruta):
        self._ruta = ruta

    @property
    def archivo(self):
        return self._archivo

    @archivo.setter
    def archivo(self, archivo):
        self._archivo = archivo

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, numero):
        self._numero = numero

    def __str__(self):
        with open(f"{os.sep.join(self._ruta.split('|'))}{os.sep}{self._archivo}",
                  'rb') as ar:
            te = ar.read()
        by = base64.b64encode(te)
        return by.decode('utf-8')


class Utilidades:
    @staticmethod
    def no_vacio(texto):
        if not texto:
            return 'NA'
        else:
            return texto

    @staticmethod
    def seis_decimales(valor):
        try:
            t = f'{float(valor):.6f}'
        except ValueError:
            t = '0.0'
        return t

    @staticmethod
    def dos_decimales(valor):
        try:
            t = f'{float(valor):.2f}'
        except ValueError:
            t = '0.0'
        return t


class Configuracion:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(r'facturaciononline\conf.ini', encoding='utf-8')
        self.ruta_general = config['Rutas'].get('general')
        self.ruta_cert = config['Rutas'].get('certificado')
        self.ruta_llave = config['Rutas'].get('llave')
        self.ruta_xslt = config['Rutas'].get('xslt')
        self.user = config['IENTC'].get('user')
        self.pswd = config['IENTC'].get('pswd')
        self.url_auth = config['IENTC'].get('url_auth')
        self.url_timbre = config['IENTC'].get('url_timbre')
        self.url_cuenta = config['IENTC'].get('url_cuenta')

    def ruta(self, ruta):
        if ruta == 'certificado':
            return os.sep.join([self.ruta_general, self.ruta_cert])
        elif ruta == 'llave':
            return os.sep.join([self.ruta_general, self.ruta_llave])
        elif ruta == 'xslt':
            return os.sep.join([self.ruta_general, self.ruta_xslt])


class CFDIError(Exception):
    pass
