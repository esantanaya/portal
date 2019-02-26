from django import forms

CHOICES_DATOS = [
    ('000', 'Uso CFDI'),
    ('G01', 'Adquisición de mercancias'),
    ('G02', 'Devoluciones, descuentos o bonificaciones'),
    ('G03', 'Gastos en general'),
    ('I01', 'Construcciones'),
    ('I02', 'Mobilario y equipo de oficina por inversiones'),
    ('I03', 'Equipo de transporte'),
    ('I04', 'Equipo de computo y accesorios'),
    ('I05', 'Dados, troqueles, moldes, matrices y herramental'),
    ('I06', 'Comunicaciones telefónicas'),
    ('I07', 'Comunicaciones satelitales'),
    ('I08', 'Otra maquinaria y equipo'),
    ('D01', 'Honorarios médicos, dentales y gastos hospitalarios.'),
    ('D02', 'Gastos médicos por incapacidad o discapacidad'),
    ('D03', 'Gastos funerales.'),
    ('D04', 'Donativos.'),
    ('D05', 'Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación).'),
    ('D06', 'Aportaciones voluntarias al SAR.'),
    ('D07', 'Primas por seguros de gastos médicos.'),
    ('D08', 'Gastos de transportación escolar obligatoria.'),
    ('D09', 'Depósitos en cuentas para el ahorro, primas que tengan como base planes de pensiones.'),
    ('D10', 'Pagos por servicios educativos (colegiaturas)'),
    ('P01', 'Por definir'),
]


class ConsultaForm(forms.Form):
    concesionaria = forms.ChoiceField(label='Concesionario', choices=[('QMO710112RH2', 'QUERETARO MOTORS')])
    factura = forms.CharField(label='Factura')
    total = forms.DecimalField(label='Total', min_value=0)


class DatosForm(forms.Form):
    idCertificado = forms.CharField(widget=forms.HiddenInput())
    agencia = forms.CharField(widget=forms.HiddenInput())
    rfc = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'R.F.C.'}))
    uso_cfdi = forms.ChoiceField(choices=CHOICES_DATOS, required=True)
    razon_social = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Razón Social'}))
    calle = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Calle y número'}))
    cp = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'C.P.'}))
    colonia = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Colonia'}))
    municipio = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Municipio'}))
    estado = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Estado'}))
