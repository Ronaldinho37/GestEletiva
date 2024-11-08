from django.shortcuts import render
from ..views import dados_universsais,menssagem_var
from ..models import Professores
from .funcoes_sem_url.definir_user import definir_user
from .funcoes_sem_url.pagina_pode_funcionar import ver_se_a_pagina_pode_funcionar
#função que retorna para a página dos tutores
def tutoria(request):
    try:
        if request.session['user'] != dados_universsais['user']:
            dados = definir_user(request)
        else:
            dados=dados_universsais.copy()
    except:
        dados = definir_user(request)
    #verificando se a página pode funcionar
    if ver_se_a_pagina_pode_funcionar('tutoria',dados) == True:
        return render(request,'definir_as_paginas/acesso_bloqueado.html',dados)
    dados['pagina'] = 'tutoria' #excluir essa linha
    #pegue do models dos Professores somente onde tutor for igual a True
    dados['tutores'] = Professores.objects.filter(tutor=True)
    try:
        dados['message'] = menssagem_var['mensagem'] 
        menssagem_var['mensagem'] = ""
    except:
        dados['message'] = ""
    #retornando para a página de tutoria
    return render(request,'principais/tutoria.html',dados)