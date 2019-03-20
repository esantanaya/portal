class Comprobante:
    def __init__(
        self,
        nombre_archivo,
        no_certificado,
        fecha,
        folio,
        lugar_expedicion,
        moneda,
        sello,
        serie,
        subtotal,
        tipo_comprobante,
        total,
        version,
        emisor,
        receptor,
        forma_pago=None,
        metodo_pago=None,
        conceptos=None,
        pagos=None,
        timbre=None,
        total_letra=None,
        cuenta_pago=None,
        vehiculo=None,
    ):
        self._nombre_archivo = nombre_archivo
        self._no_certificado = no_certificado
        self._fecha = fecha
        self._folio = folio
        self._lugar_expedicion = lugar_expedicion
        self._moneda = moneda
        self._sello = sello
        self._serie = serie
        self._subtotal = subtotal
        self._tipo_comprobante = tipo_comprobante
        self._total = total
        self._version = version
        self._emisor = emisor
        self._receptor = receptor
        self._forma_pago = forma_pago
        self._metodo_pago = metodo_pago
        self._conceptos = conceptos
        self._pagos = pagos
        self._timbre = timbre
        self._total_letra = total_letra
        self._cuenta_pago = cuenta_pago
        self._vehiculo = vehiculo

    @property
    def nombre_archivo(self):
        return self._nombre_archivo

    @nombre_archivo.setter
    def nombre_archivo(self, nombre_archivo):
        self._nombre_archivo = nombre_archivo

    @property
    def no_certificado(self):
        return self._no_certificado

    @no_certificado.setter
    def no_certificado(self, no_certificado):
        self._no_certificado = no_certificado

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

    @property
    def tipo_comprobante(self):
        return self._tipo_comprobante

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
    def timbre(self):
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
    def vehiculo(self):
        return self._vehiculo

    @vehiculo.setter
    def vehiculo(self, vehiculo):
        self._vehiculo = vehiculo


class Vehiculo:
    def __init__(self):
        self._marca = ''
        self._modelo = ''
        self._anio = ''
        self._color = ''
        self._serie = ''
        self._kilometraje = ''
        self._placas = ''
        self._motor = ''
        self._bonete = ''
        self._referencia = ''
        self._recepcionista = ''
        self._siniestro = ''

    @property
    def marca(self):
        return self._marca

    @marca.setter
    def marca(self, marca):
        self._marca = marca

    @property
    def modelo(self):
        return self._modelo

    @modelo.setter
    def modelo(self, modelo):
        self._modelo = modelo

    @property
    def anio(self):
        return self._anio

    @anio.setter
    def anio(self, anio):
        self._anio = anio

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def serie(self):
        return self._serie

    @serie.setter
    def serie(self, serie):
        self._serie = serie

    @property
    def kilometraje(self):
        return self._kilometraje

    @kilometraje.setter
    def kilometraje(self, kilometraje):
        self._kilometraje = kilometraje

    @property
    def placas(self):
        return self._placas

    @placas.setter
    def placas(self, placas):
        self._placas = placas

    @property
    def motor(self):
        return self._motor

    @motor.setter
    def motor(self, motor):
        self._motor = motor

    @property
    def bonete(self):
        return self._bonete

    @bonete.setter
    def bonete(self, bonete):
        self._bonete = bonete

    @property
    def referencia(self):
        return self._referencia

    @referencia.setter
    def referencia(self, referencia):
        self._referencia = referencia

    @property
    def recepcionista(self):
        return self._recepcionista

    @recepcionista.setter
    def recepcionista(self, recepcionista):
        self._recepcionista = recepcionista

    @property
    def siniestro(self):
        return self._siniestro

    @siniestro.setter
    def siniestro(self, siniestro):
        self._siniestro = siniestro


class Emisor:
    def __init__(
        self,
        nombre,
        regimen_fiscal,
        rfc,
        calle_numero=None,
        colonia=None,
        ciudad=None,
        estado_pais=None,
        codigo_postal=None,
    ):
        self._nombre = nombre
        self._regimen_fiscal = regimen_fiscal
        self._rfc = rfc
        self._calle_numero = calle_numero
        self._colonia = colonia
        self._ciudad = ciudad
        self._estado_pais = estado_pais
        self._codigo_postal = codigo_postal

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
    def __init__(self, cantidad, clave_prod_serv, clave_interna, clave_unidad,
                 descripcion, importe, valor_unitario):
        self._cantidad = cantidad
        self._clave_prod_serv = clave_prod_serv
        self._clave_interna = clave_interna
        self._clave_unidad = clave_unidad
        self._descripcion = descripcion
        self._importe = importe
        self._valor_unitario = valor_unitario

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, cantidad):
        self._cantidad = cantidad

    @property
    def clave_prod_serv(self):
        return self._clave_prod_serv

    @clave_prod_serv.setter
    def clave_prod_serv(self, clave_prod_serv):
        self._clave_prod_serv = clave_prod_serv

    @property
    def clave_interna(self):
        return self._clave_interna

    @clave_interna.setter
    def clave_interna(self, clave_interna):
        self._clave_interna = clave_interna

    @property
    def clave_unidad(self):
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
