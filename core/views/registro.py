# core/views/registro.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db import transaction
from ..forms.form_registro import VeterinarioRegistrationForm
from ..forms.form_veterinario import CrmvForm
from ..forms.form_cadastros_gerais import EnderecoForm
from ..models import CodigoAcesso

def registro_veterinario(request):
    if request.method == 'POST':
        vet_form = VeterinarioRegistrationForm(request.POST, prefix='vet')
        crmv_form = CrmvForm(request.POST, prefix='crmv')
        endereco_form = EnderecoForm(request.POST, prefix='endereco')

        if vet_form.is_valid() and crmv_form.is_valid() and endereco_form.is_valid():
            with transaction.atomic():
                endereco = endereco_form.save()
                crmv = crmv_form.save()
                
                veterinario = vet_form.save(commit=False)
                veterinario.endereco = endereco
                veterinario.crmv = crmv
                
                codigo_acesso_str = vet_form.cleaned_data.get('codigo_acesso')
                codigo_acesso = CodigoAcesso.objects.get(codigo=codigo_acesso_str)
                veterinario.codigo_acesso = codigo_acesso
                
                veterinario.save()

                codigo_acesso.utilizado = True
                codigo_acesso.save()
            
            login(request, veterinario)
            return redirect('index')
    else:
        vet_form = VeterinarioRegistrationForm(prefix='vet')
        crmv_form = CrmvForm(prefix='crmv')
        endereco_form = EnderecoForm(prefix='endereco')

    context = {
        'vet_form': vet_form,
        'crmv_form': crmv_form,
        'endereco_form': endereco_form,
    }
    return render(request, 'core/registro/registro.html', context)