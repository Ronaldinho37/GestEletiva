from django.shortcuts import render, redirect
from ..views import menssagem_var,dados_universsais
from .funcoes_sem_url.para_onde_vou import para_onde_vou
from .funcoes_sem_url.acao_requisitada import verificar_se_o_usuario_pode_realizar_a_acao_equisitada
from ..models import PaginasUtilizaveis
def definir_paginas_utilizaveis(request):
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'definirpaginas') == True:
        return redirect("/")
    #recebe todos os objects presentes no models "PaginasUtilizaveis"
    ObjectPagina = PaginasUtilizaveis.objects
    if request.method == 'POST':
        link_antigo = request.POST.get('link_antigo')
        #O models "PaginasUtilizaveis" só tem um valor
        ObjectPagina = ObjectPagina.get(id=1)
        #lista com todas as páginas
        paginas_list = ['tutoria','eletiva','index','sobre']
        #percorrendo as páginas
        for i in paginas_list:
            #pegando os valores dos inputs no html
            request_da_vez = request.POST.get(f'{i}')
            #se for igual a 'on' é porque ele foi marcado
            if request_da_vez == 'on':
                #se a página da vez for tutoria então altere-a, e assim por diante. True: página pode ser utilizada, False: página não pode ser utilizada.
                if i == 'tutoria':
                    ObjectPagina.tutoria = True
                elif i == 'eletiva':
                    ObjectPagina.eletiva = True
                elif i == 'index':
                    ObjectPagina.index = True
                elif i == 'sobre':
                    ObjectPagina.sobre = True
            else:
                if i == 'tutoria':
                    ObjectPagina.tutoria = False
                elif i == 'eletiva':
                    ObjectPagina.eletiva = False
                elif i == 'index':
                    ObjectPagina.index = False
                elif i == 'sobre':
                    ObjectPagina.sobre = False
        #salvando as alterações
        ObjectPagina.save()
        #dizendo que alterções foram feitas
        menssagem_var['mensagem'] = "Alterações efetuadas com sucesso!"
        return para_onde_vou(request,link_antigo)
    else:
        dados = dados_universsais.copy()
        #pegando os valores do object de id igual a 1
        valores_do_object = ObjectPagina.values().get(id=1)
        #percorrendo os valores
        for i in valores_do_object:
            #se for igual a true, crie uma variável no dict dados e defina-a como "checked", no html isso equivale a "marcado"
            if valores_do_object[f'{i}'] == True:
                dados[f'{i}'] = 'checked'
            else:
                dados[f'{i}'] = ''
       
        return render(request,'definir_as_paginas/definir_paginas.html',dados)