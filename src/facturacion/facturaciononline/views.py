import os
from zipfile import ZipFile
from io import BytesIO
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMessage

from .forms import ConsultaForm, DatosForm, CorreoForm
from .legacy_db import (consulta_valides, datos_cliente, get_cab_comp,
                        get_impuestos, get_conceptos, get_fecha_comp)
from .comprobante import Receptor, Emisor, Comprobante, Impuestos, Concepto


def corrige_factura(factura):
    return f'{factura[0:2]}{int(factura[2:]):05d}'.upper()


def consulta_carga(request):
    titulo = 'Facturación en Línea'
    form = ConsultaForm()
    context = {
        'titulo': titulo,
        'form': form,
    }
    if request.method == 'POST':
        context['error'] = 'No fue posible localizar la factura'
    return render(request, 'facturaciononline/consulta.html', context)


def consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            agencia = form.cleaned_data['concesionaria']
            try:
                factura = corrige_factura(form.cleaned_data['factura'])
            except IndexError:
                return HttpResponseRedirect('/facturaciononline/')
            except ValueError:
                return HttpResponseRedirect('/facturaciononline/')
            total = form.cleaned_data['total']
            resp = consulta_valides(agencia, factura, total)
            if not resp:
                return HttpResponseRedirect('/facturaciononline/')
            elif isinstance(resp, tuple):
                fecha = get_fecha_comp(agencia, factura)
                context = {
                    'titulo': 'Descarga de Información',
                    'agencia': agencia,
                    'idCertificado': resp[1],
                    'mes_anio': fecha.strftime('%m%Y'),
                    'correo_form': CorreoForm({
                        'agencia': agencia,
                        'idCertificado': resp[1],
                        'mes_anio': fecha.strftime('%m%Y')
                    }),
                }
                return render(request, 'facturaciononline/descarga.html',
                              context)
            else:
                res_dat_cl = datos_cliente(agencia, resp)
                rfc, nombre, calle, cp, colonia, mun, estado = res_dat_cl
                data = {
                    'idCertificado': resp,
                    'agencia': agencia,
                    'rfc': rfc,
                    'razon_social': nombre,
                    'calle': calle,
                    'cp': cp,
                    'colonia': colonia,
                    'municipio': mun,
                    'estado': estado,
                }
                d_form = DatosForm(data)
                context = {
                    'titulo': 'Datos Físcales',
                    'idCertificado': resp,
                    'form': d_form,
                }
                return render(request, 'facturaciononline/datos.html', context)


def timbre(request):
    if request.method == 'POST':
        form = DatosForm(request.POST)
        if form.is_valid():
            agencia = form.cleaned_data['agencia']
            id_comp = form.cleaned_data['idCertificado']
            receptor = Receptor(
                form.cleaned_data['razon_social'],
                form.cleaned_data['rfc'],
                form.cleaned_data['uso_cfdi'],
                calle=form.cleaned_data['calle'],
                colonia=form.cleaned_data['colonia'],
                municipio=form.cleaned_data['municipio'],
                estado=form.cleaned_data['estado'],
                pais='México',
                codigo_postal=form.cleaned_data['cp'],
            )
            emisor = Emisor(agencia)
            datos_cab = get_cab_comp(agencia, id_comp)
            datos_imp = get_impuestos(agencia, id_comp)
            impuesto = Impuestos(datos_imp[2], '002', datos_imp[1], 'Tasa')
            comprobante = Comprobante(
                id_comp,
                datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                datos_cab[1],
                datos_cab[2],
                str(datos_cab[3]),
                str(datos_cab[4]),
                'ingreso',
                '3.3',
                emisor,
                receptor,
                datos_cab[5],
                datos_cab[6],
                datos_cab[7],
                datos_cab[8],
                impuesto,
            )
            datos_con = get_conceptos(agencia, id_comp)
            fecha = get_fecha_comp(agencia, id_comp)
            conceptos = []
            for reg in datos_con:
                tasa = 0.160000
                concepto = Concepto(reg[0], reg[3], reg[1], reg[5],
                                    reg[7], reg[6], '002', tasa,
                                    reg[8], reg[7], 'Tasa')
                conceptos.append(concepto)
            comprobante.conceptos = conceptos
            comprobante.timbra_xml()
            context = {
                'titulo': 'Descarga de Información',
                'agencia': agencia,
                'idCertificado': id_comp,
                'mes_anio': fecha.strftime('%m%Y'),
                'correo_form': CorreoForm({
                    'agencia': agencia,
                    'idCertificado': id_comp,
                    'mes_anio': fecha.strftime('%m%Y'),
                }),
            }
            return render(request, 'facturaciononline/descarga.html', context)


def zipper(request):
    if request.method == 'GET':
        info_ars = request.GET
        agencia = info_ars['agencia']
        mes_anio = info_ars['mes_anio']
        archivo = info_ars['archivo']
        ruta_archivo = os.path.join('facturaciononline', 'static', 'facturas',
                                    agencia, mes_anio, archivo)
        filenames = [f'{ruta_archivo}.xml', f'{ruta_archivo}.pdf']
        b = BytesIO()

        zip = ZipFile(b, 'w')

        for ruta in filenames:
            path_archivo, real_archivo = os.path.split(ruta)
            zip.write(ruta, os.path.join('factura', real_archivo))
        zip.close()

        resp = HttpResponse(
            b.getvalue(),
            content_type='application/x-zip-compressed',
        )
        resp['Content-Disposition'] = f'attachment; filename={archivo}.zip'
        return resp


def envio_correo(request):
    if request.method == 'POST':
        form = CorreoForm(request.POST)
        if form.is_valid():
            archivo = form.cleaned_data['idCertificado']
            agencia = form.cleaned_data['agencia']
            mes_anio = form.cleaned_data['mes_anio']
            ruta_archivo = os.path.join('facturaciononline', 'static',
                                        'facturas', agencia, mes_anio, archivo)
            email = EmailMessage(
                'Su factura',
                'Le enviamos su factura',
                'facturas@prolecsa.mx',
                [form.cleaned_data['correo']],
            )
            email.attach_file(f'{ruta_archivo}.pdf')
            email.attach_file(f'{ruta_archivo}.xml')
            email.send()
        return HttpResponseRedirect('/facturaciononline/')
