from django.shortcuts import render,redirect
from ..forms import LoginForm
from ..models import Admins
from django.contrib.auth import login, authenticate
from ..views import dados_universsais,menssagem_var
from .funcoes_sem_url.para_onde_vou import para_onde_vou
#nesta função é feito o login dos usuários 
def login_viwes(request):
    try:
        request.session['user']
    except:
        request.session['user'] = None
    #esse if verifica se já tem um usuário logado, se tiver é necessário que deslogue para logar de novo
    if request.session['user'] == 'ADMIN'or request.session['user'] != None:
        menssagem_var['mensagem'] = 'Já tem um usuário logado'
        return redirect("/")
    
    if request.method == 'POST':
        #variável que guarda o valor do nome inserido no input do login
        nome = request.POST.get('nome').lower()
        #variável que guarda a senha inserida no input do login
        password = request.POST.get('password')
        link_antigo = request.POST.get('link_antigo')
        #guardará o valor inserido pelo usuário referente a cada checkbox
        checkboxes = {}
        #lista de nomes de cada checkbox do html
        lista_checkboxes = ['ADMIN','Admin']
        #for que armazena na variável 'checkboxes' os valores referentes a cada input do html
        for i in lista_checkboxes:
            checkboxes[f'{i}'] = request.POST.get(f'{i}')
        #caso o usuário a ser logado seja o ADMIN
        if checkboxes['ADMIN'] == 'on':
            #verifique se ele existe no Django
            usuario = authenticate(username=nome,password=password)
            #se existir
            if usuario is not None:
                #logue-o no Django
                login(request,usuario)
                request.session['user'] = 'ADMIN'
                request.session['nome_user_logado'] = nome
                request.session['senha_user_logado'] = password
                menssagem_var['mensagem'] = "Usuário logado com sucesso!"
                return para_onde_vou(request,link_antigo)
        #caso o usuário a ser logado seja o Admin
        elif checkboxes['Admin'] == 'on':
            #pegue todos os admin do meu site
            admins = Admins.objects.all().values()
            #percorra-os
            for i in admins:
                #se o nome e senha pegados do html forem iguais à nome e senha de algum admin então logue-o
                if i['nome'].lower() == nome and i['senha'] == password:
                    request.session['user'] = 'admin'
                    #a lista de ações permitidas ao usuário estão no models com string, o split() transforma a string em uma lista
                    acoes_lista = i['acoes'].split()
                    request.session['lista_de_acoes'] = acoes_lista
                    request.session['nome_user_logado'] = nome
                    request.session['senha_user_logado'] = password
                    menssagem_var['mensagem'] = "Usuário logado com sucesso!"
                    return para_onde_vou(request,link_antigo) 
        #se chegou até aqui é porque nenhum dos ifs anteriores foram iguais a True, logo a senha ou nome ou usuário escolhidos não coincidem
        dados = {}
        dados['message'] = "Usuário ou senha inválidos!, por favor, preencha noamente suas credenciais!!"
        dados['form'] = LoginForm()
        dados['nome'] = nome
        dados['password'] = password
        return render(request,'principais/login.html',dados)
        
        
    else:
        dados = dados_universsais.copy()
        dados['message'] = ''
        return render(request,'principais/login.html',dados)
    