from django.shortcuts import render
from ..views import dados_universsais,menssagem_var,definir_user,ver_se_a_pagina_pode_funcionar
#função que retorna para a página sobre(about)
def sobre(request):
    try:
        if request.session['user'] != dados_universsais['user']:
            dados = definir_user(request)
        else:
            dados=dados_universsais.copy()
    except:
        dados = definir_user(request)
     #verificando se a página pode funcionar
    if ver_se_a_pagina_pode_funcionar('sobre',dados) == True:
        return render(request,'definir_as_paginas/acesso_bloqueado.html',dados)
    dados['pagina'] = 'sobre'#excluir essa linha
    try:
        dados['message'] = menssagem_var['mensagem']
        menssagem_var['mensagem'] = ""
    except:
        dados['message'] = ""
    return render(request,'principais/about.html',dados)