from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import ConsultaForm, DatosForm
from .legacy_db import (consulta_valides, datos_cliente, get_cab_comp,
                        get_impuestos, get_lugar_expedicion, get_conceptos)
from .comprobante import Receptor, Emisor, Comprobante, Impuestos, Concepto


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
            factura = form.cleaned_data['factura']
            total = form.cleaned_data['total']
            resp = consulta_valides(agencia, factura, total)
            if not resp:
                return HttpResponseRedirect('/facturaciononline/')
            elif type(resp) == 'Tuple':
                return HttpResponseRedirect('/')
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
                datos_cab[0].strftime('%Y-%m-%dT%H:%M:%S'),
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
            conceptos = []
            for reg in datos_con:
                importe = reg[0] * reg[6]
                tasa = 0.160000
                concepto = Concepto(reg[0], reg[3], reg[1], reg[5],
                                    importe , reg[6], '002', tasa,
                                    float(importe) * tasa, importe, 'Tasa')
                conceptos.append(concepto)
            comprobante.conceptos = conceptos
            arbol = comprobante.crea_xml()
