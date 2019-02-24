from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def consulta(request):
    titulo = 'Facturación en Línea'
    context = {'titulo': titulo}
    template_consulta = loader.get_template('facturaciononline/base.html')
    return  HttpResponse(template_consulta.render(context, request))
