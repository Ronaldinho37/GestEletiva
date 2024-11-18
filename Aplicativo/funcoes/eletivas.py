from ..models import Eletivas,Professores,CarrosselProfessores
from ..views import dados_universsais,menssagem_var
from .funcoes_sem_url.definir_user import definir_user
from django.shortcuts import render
from .funcoes_sem_url.pagina_pode_funcionar import ver_se_a_pagina_pode_funcionar

#função que retorna para a página das eletivas com as eletivas presentes no site
def eletivas(request):
    try:
        if request.session['user'] != dados_universsais['user']:
            dados = definir_user(request)
        else:
            dados=dados_universsais.copy()
    except:
        dados = definir_user(request)
    if ver_se_a_pagina_pode_funcionar('eletiva',dados) == True:
        return render(request,'definir_as_paginas/acesso_bloqueado.html',dados)
    dados['pagina'] = "eletivas"
    dados['eletivas'] = Eletivas.objects.all().values()
    #essa variável recebe as duplas de professores por eletivas
    todos_professores = {}
    #for que percorre as eletivas existente
    #ao fim, é adicionado na variável 'dados['todos_professores']' um dict com cada par de professores por eletiva
    #no template é chamada uma tag que filtra o dict e retorna o nome dos professores que estão na eletiva
    for i in dados['eletivas']:
        #filtra os professores que dão aula na eletiva
        #e adiciona-os na variável "todos_professores" com uma key referente ao nome da eletiva 
        todos_professores[f"professor_de_{i['titulo']}"] = Professores.objects.filter(eletiva=f"{i['titulo']}").values()
    #adiciono a variável 'todos_professores' a variável dados
    dados['todos_professores'] = todos_professores
    try:
        dados['message'] = menssagem_var['mensagem']
        menssagem_var['mensagem'] = ""
    except:
        dados['message'] = ""
    dados['carrossel'] = []
    try:
        carrossel = CarrosselProfessores.objects.get(id=1).ids
        lista_ids = carrossel.split(',')
    except:
        carrossel = ''

    if carrossel != '':
        for i in lista_ids:
            professor_carrossel = Professores.objects.get(id=int(i))
            dados['carrossel'].append(professor_carrossel)
    return render(request,'eletiva/eletivas.html',dados)