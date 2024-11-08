from ..views import menssagem_var, dados_universsais
from .funcoes_sem_url.definir_user import definir_user
from .funcoes_sem_url.pagina_pode_funcionar import ver_se_a_pagina_pode_funcionar
from ..models import OqueTemosaOferecer,Anuncio
from django.shortcuts import render
def retornar_index(request):
    try:
        if request.session['user'] != dados_universsais['user']:
            dados = definir_user(request)
        else:
            dados=dados_universsais.copy()
    except:
        dados = definir_user(request)
    if ver_se_a_pagina_pode_funcionar('index',dados) == True:
        return render(request,'definir_as_paginas/acesso_bloqueado.html',dados)
    #variável que contém os cards de avisos
    dados['avisos'] = Anuncio.objects.all().order_by("-id")[:2]
    dados['OqueTemosaOferecer'] = OqueTemosaOferecer.objects.all().values()
    try:
        dados['message'] = menssagem_var['mensagem']
        menssagem_var['mensagem'] = ""
    except:
        dados['message'] = ""
    return render(request,'principais/index.html',dados)