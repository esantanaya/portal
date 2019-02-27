import mysql.connector
from math import ceil


def consulta_valides(agencia, factura, total):
    try:
        t_min = total - 1
        t_max = total + 1
        factura = f'{factura[0:2]}{int(factura[2:]):05d}'.upper()
        con = mysql.connector.connect(host='192.168.24.10', user='root', passwd='srvsql0981', database='certificadosfiscalesdigitales')
    except Exception as e:
        pass
    else:
        query = f"select c.idCertificado, tc.idCertificado from certificados c left join timbrecertificado tc on tc.idEmisor = c.idEmisor and tc.idCertificado = c.idCertificado where c.idEmisor = '{agencia}' and c.idCertificado = '02-UD10001-{factura}' and c.total between {t_min} and {t_max}"
        cur = con.cursor()
        cur.execute(query)
        resultados = [_ for _ in cur]
        cur.close()
        con.close()
        if len(resultados) == 1:
            cer, tim = resultados[0]
            if cer is not None and tim is None:
                return cer
            elif cer is not None and tim is not None:
                return (True, cer)
            else:
                return False
        else:
            return False


def datos_cliente(agencia, idCertificado):
    con = mysql.connector.connect(host='192.168.24.10', user='root', passwd='srvsql0981', database='certificadosfiscalesdigitales')
    query = ("select idReceptor, nombre, calle, codigoPostal, colonia, "
             "municipio, estado from receptorcertificado "
             f"where idEmisor = '{agencia}' "
             f"and idCertificado = '{idCertificado}'")
    cur = con.cursor()
    cur.execute(query)
    resultados = [_ for _ in cur]
    cur.close()
    con.close()
    if len(resultados) == 1:
        return resultados[0]

def get_emisor(idEmisor):
    con = mysql.connector.connect(host='192.168.24.10', user='root',
                                  passwd='srvsql0981',
                                  database='certificadosfiscalesdigitales')
    query = ("select idEmisor, nombre, calle, numeroExterior, numeroInterior, "
             "colonia, municipio, estado, pais, codigoPostal, '601', "
             "numeroCertificado, nombreArchivoCertificado, nombreArchivoLlave,"
             " passwordArchivoLlave from emisores "
             f"where idEmisor = '{idEmisor}'")
    cur = con.cursor()
    cur.execute(query)
    resultado = cur.fetchone()
    return resultado

def get_cab_comp(idEmisor, idCertificado):
    con = mysql.connector.connect(host='192.168.24.10', user='root',
                                  passwd='srvsql0981',
                                  database='certificadosfiscalesdigitales')
    query = ("select fecha, serie, folio, subtotal, total, formaDePago, "
             "metodoDePago, cadenaTotal, numeroCuentaPago from certificados "
             f"where idEmisor = '{idEmisor}' and idCertificado = "
             f"'{idCertificado}'")
    cur = con.cursor()
    cur.execute(query)
    resultado = cur.fetchone()
    return resultado

def get_impuestos(idEmisor, idCertificado):
    con = mysql.connector.connect(host='192.168.24.10', user='root',
                                  passwd='srvsql0981',
                                  database='certificadosfiscalesdigitales')
    query = ("select impuesto, tasa, importe from impuestoscertificado "
             f"where idEmisor = '{idEmisor}' and idCertificado ="
             f" '{idCertificado}'")
    cur = con.cursor()
    cur.execute(query)
    resultado = cur.fetchone()
    return resultado

def get_lugar_expedicion(idEmisor, sucursal):
    con = mysql.connector.connect(host='192.168.24.10', user='root',
                                  passwd='srvsql0981',
                                  database='certificadosfiscalesdigitales')
    query = ("select cp from sucursalesemisores where idEmisor = "
             f"'{idEmisor}' and sucursal = '{sucursal}'")
    cur = con.cursor()
    cur.execute(query)
    resultado = cur.fetchone()
    return resultado[0]

def get_conceptos(idEmisor, idCertificado):
    con = mysql.connector.connect(host='192.168.24.10', user='root',
                                  passwd='srvsql0981',
                                  database='certificadosfiscalesdigitales')
    query = ("select cantidad, clave_unidad, unidad, clave_prod_serv,"
             " numeroIdentificacion, descripcion, valorUnitario, importe, "
             "impuesto from conceptoscertificados where idEmisor = "
             f"'{idEmisor}' and idCertificado = '{idCertificado}'")
    cur = con.cursor()
    cur.execute(query)
    resultado = cur.fetchall()
    return resultado
