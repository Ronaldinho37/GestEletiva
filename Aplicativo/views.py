import django
import django.contrib
import django.contrib.messages
from django.shortcuts import render,redirect,get_object_or_404
from .forms import LoginForm,AddEletivaForm, AnuncioForm, UpdateEletiva
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .models import Alunos,Admins,Professores,Eletivas,Anuncio
from django.contrib import messages
import os
from PIL import Image
#pip freeze > requiriments.txt

#esta variável receberá o valor que eu precisarei em todas as funções, ela server para eu não ter que ficar
#repetindo linhas de código. Em quase todas as funções a variável 'dados' hospedará o valor dela.
dados_universsais = {}
# roni
# r@ni
# ImgCarrossel.objects.all().delete()
#1920 x 695 
# Create your views here.

#como codificar palavras
# import rsa
# (publickey, privatekey) = rsa.newkeys(100)
# m = "oi".encode('utf8')
# ciphertext = rsa.encrypt(m, publickey)
# m2 = rsa.decrypt(ciphertext, privatekey)
# print(ciphertext)
#esta função serve para verificar se a imagem a ser adicionada é existente se não for a adicionará 
#se for então será adicionado o caminho referente a ela
def checar_imagem_existente(imagem,pasta,acao):
    #este if adiciona as imagens padrões caso a variável "imagem" seja igual a None 
    if imagem == None:
        #caso seja uma imagem da dupla de professores
        if pasta == 'img_eletivas/img_professores_eletiva':
            return f'{pasta}/Professorpadrao.jpg'
        #caso seja um user
        else:
            return 'img_fixas/anonimo.png'
    #se chegou até aqui é porque nenhum dos ifs acima foi verdadeiro, logo a imagem inserida não é igual a None
    #o único jeito que consegui verificar se a imagem não é igual às demais foi transformando-as em bytes
    #esta variável recebe os bytes equivalentes a imagem inserida
    nova_imagem = Image.open(imagem).tobytes("xbm", "rgb")
    #esse try server para pegar todas as imagens da pasta passada como parâmetro
    #se a pasta não existir então irá retornar a imagem
    try:
        #variável que contém todos os itens da pasta requisitada, em forma de lista
        pasta_da_velha_imagem = os.listdir(f'{os.getcwd()}/media/{pasta}')
    except:
        return imagem
    #essa variável serve para eu ter um controle do que esta acontecendo, mais a frente ele dirá se eu tenho ou não de adicionar a imagem
    tam = 0
    #for que percorre a variável "pasta_da_velha_imagem"
    for e in pasta_da_velha_imagem:
        #esse if é importante pois "img_professores_eletiva" não é uma imagem mas sim uma pasta
        if e !=  'img_professores_eletiva':
            #essa variável receberá todas as imagens da pasta em forma de bytes, uma por vez 
            imagem_da_pasta = Image.open(f'{os.getcwd()}/media/{pasta}/{e}').tobytes("xbm", "rgb")
            #caso a "imagem_da_pasta" for igual a "nova_imagem" esse if retornará o caminho referente a mesma
            if nova_imagem == imagem_da_pasta:
                return f'{pasta}/{e}'
        #se as imagens não forem iguais então será agregado valor à variável de controle
        tam += 1
    #se a variável de controle for igual a 0 é porque nenhuma das imagens é igual a imagem inserida pelo user
    #se a quantidade de itens da variável "pasta_da_velha_imagem" for igual a 0 é porque não tem imagem na pasta
    #logo se ambas ou apenas uma for verdadeira o código retornará a imagem 
    if tam != 0 or len(pasta_da_velha_imagem) == 0:
        return imagem
#esta função excluirá as imagens inutilizadas
#dir = Pasta que está localizado a imagem a ser excluída
#model = Valores do model django passado como parâmetro
def excluir_imagem(dir,model):
    #variável que guarda as imagens que estão sendo utilizadas
    imagens_usuarios = []
    #variável que guarda todas imagens da pasta media
    imagens_da_pasta_solicitada = os.listdir(f'{os.getcwd()}/media/{dir}')
    #caso a pasta passada como parâmetro seja a 'pasta_da_velha_imagem' é necessário que se exclua a sub-pasta 'img_professores_eletiva', pois eu só preciso das imagens
    if dir == 'img_eletivas':
        imagens_da_pasta_solicitada.remove('img_professores_eletiva')
    #essa variável tem nome de 'coluna_da_vez' pois na maioria dos models o nome da coluna referente a imagem é 'imagem'
    #e em Eletivas o nome é 'img_professores_eletiva'
    coluna_da_vez = ''
    #esse if remove a imagem padrão da lista caso a pasta(dir) for 'img_eletivas/img_professores_eletiva'
    #e atribui a variável 'coluna_da_vez' o nome da coluna 'img_professores_eletiva'
    if dir == 'img_eletivas/img_professores_eletiva':
        imagens_da_pasta_solicitada.remove('Professorpadrao.jpg')
        coluna_da_vez += 'img_professores_eletiva'
    #como só é um model que usa um nome de coluna diferente então se o if acima for False será atribuído a variável 'coluna_da_vez' o valor 'imagem'   
    else:
        coluna_da_vez += 'imagem'
    #for que percorre o model possibilitando obter cada imagem usada no moedel
    for i in model:
        #if que atribui a variável 'imagens_usuarios' as imagens que estão sendo usadas
        if i[coluna_da_vez] != None and i[coluna_da_vez] not in imagens_usuarios:
            #ao ser adicionado uma imagem ela receberá o seguinte valor: pasta/imagem(pasta: para onde ele vai; imagem: a imagem)
            #porém como eu só quero a imagem, essa linha exclui o nome da pasta e adiciona somente o nome da imagem a variável 'imagens_usuarios'
            img = i[coluna_da_vez].replace(f'{dir}/','')
            imagens_usuarios.append(img)
    #for que percorre as imagens da pasta(dir)
    for i in imagens_da_pasta_solicitada:
        #se a imagem da pasta não esta em 'imagens_usuarios', então ela esta inutilizada portanto apague-a
        if i not in imagens_usuarios:
            os.remove(f'{os.getcwd()}/media/{dir}/{i}')
    return

#funcao que verifica se o usuário da vez pode deletar,cadastrar ou atualizar
def verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,acao):
    #recebe a classificação do user da vez. Classificação: ADMIN, admin, professor ou Aluno
    user = request.session['user']
    #True: sim saia do código e retorne ao index
    #False: não saia, pois, o usuário está abilitado a fazer seja lá o que foi requisitado
    #se o usuário não estiver logado retorna True ou seja: o usuário não pode fazer nada pois ainda não está logado
    if user == None:
        return True
    #caso o usuário for um admin tem que ser verificado se ele pode realizar a ação requisitada
    elif user == 'admin':
        #verifica se a ação existe, se existir o fluxo do código não é alterado, se não existir retorna True
        #ou seja: o usuário não pode realizar a ação pois ação não existe
        if acao in request.session['lista_de_acoes']:
            return False
        else: 
            return True
    #caso o user seja o ADMIN ele poderá fazer qualquer coisa independentemente da ação requisitada
    elif user == 'ADMIN':
        return False
    else:
        #se nenhuma dos ifs anteriores der certo então retorne True
        return True
    
def retornar_index(request):
    #############################################################
    #if que verifica se o admin já estava logado
    if request.user.is_authenticated:
        request.session['user'] = 'ADMIN'

    dados = {}
    #como a session do Django dura enquanto o navegador estiver aberto(eu abilitei para isso) 
    #quando o usuário abrir o site pela primeira vez vai dar erro, por isso esse try
    #tente pegar essa session, se ela não existir então a crie definindo-a como None ou seja nenhum usuário por enquanto
    try:
        dados['user'] = request.session['user']
    except:
        request.session['user'] = None
        dados['user'] = request.session['user']
    
    if dados_universsais != dados and dados['user'] != None:
        dados['nome_user_logado'] = request.session['nome_user_logado']
        dados['senha_user_logado'] = request.session['senha_user_logado']
        #caso o usuário for um admin então eu preciso de uma session pra cada ação que ele pode realizar
        #e esse if e for criam elas pra mim
        if dados['user'] == 'admin':
            dados['lista_de_acoes'] = request.session['lista_de_acoes']
        #atualizando a variável dos dados universsais
    dados_universsais.update(dados)
    
    
    dados['avisos'] = Anuncio.objects.all().order_by("-id")[:2]
   
    return render(request,'principais/index.html',dados)
    
def login_viwes(request):
    if request.session['user'] == 'ADMIN'or request.session['user'] != None:
        return redirect(retornar_index)
    
    if request.method == 'POST':
        nome = request.POST.get('nome').lower()
        password = request.POST.get('password')
    
        checkboxes = {}
        lista_checkboxes = ['ADMIN','Admin','Professor','Aluno','Tutor']
        for i in lista_checkboxes:
            checkboxes[f'{i}'] = request.POST.get(f'{i}')
        
        if request.session['user'] == 'ADMIN':
            logout(request)
        if checkboxes['ADMIN'] == 'on':
            usuario = authenticate(username=nome,password=password)
            if usuario is not None:
                login(request,usuario)
                request.session['user'] = 'ADMIN'
                request.session['nome_user_logado'] = nome
                request.session['senha_user_logado'] = password
                return redirect(retornar_index)
        if checkboxes['Admin'] == 'on':
            admins = Admins.objects.all().values()
            for i in admins:
                if i['nome'].lower() == nome and i['senha'] == password:
                    request.session['user'] = 'admin'
                    acoes_lista = i['acoes'].split()
                    request.session['lista_de_acoes'] = acoes_lista
                    request.session['nome_user_logado'] = nome
                    request.session['senha_user_logado'] = password
                    return redirect(retornar_index)
        
        if checkboxes['Professor'] == 'on' or checkboxes['Tutor'] == 'on':
            #irá checar se o usuário é um professor
            professor = Professores.objects.all().values()
            for i in professor:
                if i['nome'].lower() == nome and i['senha'] == password:
                    request.session['user'] = 'professor'
                    request.session['nome_user_logado'] = nome
                    request.session['senha_user_logado'] = password
                    return redirect(retornar_index)
        if checkboxes['Aluno'] == 'on':
            #irá checar se o usuário é um alunos
            alunos = Alunos.objects.all().values()
            for i in alunos:
                if i['nome'].lower() == nome and i['senha'] == password:
                    request.session['user'] = 'aluno'
                    request.session['nome_user_logado'] = nome
                    request.session['senha_user_logado'] = password
                    return redirect(retornar_index)
            
        
        dados = {}
        dados['message'] = "Usuário ou senha inválidos!"
        dados['form'] = LoginForm()
        dados['nome'] = nome
        dados['password'] = password
        return render(request,'principais/login.html',dados)
    else:
        dados = {}
        dados['message'] = ''
        return render(request,'principais/login.html',dados)

def eletivas(request):
    dados = dados_universsais.copy()
    dados['pagina'] = "eletivas"
    dados['eletivas'] = Eletivas.objects.all().values()
    todos_professores = {}
    for i in dados['eletivas']:
        todos_professores[f"professor_de_{i['titulo']}"] = Professores.objects.filter(eletiva=f"{i['titulo']}").values()
    dados['todos_professores'] = todos_professores
    dados['user'] = request.session['user']
    return render(request,'eletiva/eletivas.html',dados)

def logout_viwes(request):
    user = request.session['user'] 
    #o admin supremo(ADMIN) é o único que foi criado como um user no django e por isso ele recebe um 
    #tratamento diferente dos demais, a função logout() é própria do Django ela server para deslogar o user
    #que esta logado
    if user == 'ADMIN':
        logout(request)
    #se o usuário for um admin e quer deslogar-se então primeiro eu apago as sessions que comtém os valores 
    #das ações que ele pode realizar 
    elif user == 'admin':
        del request.session['lista_de_acoes']

    #por conseguinte eu limpo os valores da variável dos dados universais, pois ela guarda valores referentes
    # ao usuário e já que ele não está mais logado eu não preciso mais delas 
    dados_universsais.clear()
    #definindo o session 'user' como None, desta maneira o código saberá se o usuário está logado ou não
    request.session['user'] = None
    return redirect(retornar_index)


def add_eletivas(request):
    #chama a função que verifica se o usuário está apto ou não à adicionar eletivas
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
        return redirect(retornar_index)
    
    if request.method == 'POST':
        #chamando o form 
        form = AddEletivaForm(request.POST, request.FILES)
        if form.is_valid():
            #variável que armazena o nome da eletiva
            eletiva = form.cleaned_data.get('titulo')
            imagem = checar_imagem_existente(form.cleaned_data.get("imagem"),"img_eletivas",None)
            imagem_p = checar_imagem_existente(request.FILES.get("imagem_p"),"img_eletivas/img_professores_eletiva",None)
            #criando a nova eletiva
            new = Eletivas(titulo=eletiva,descricao=form.cleaned_data.get('descricao'),imagem=imagem,img_professores_eletiva=imagem_p,link=form.cleaned_data.get("link"))
            #salvando-a
            new.save()
            #redirecionando para a função que adiciona o professor responsável pela eletiva
            
            excluir_imagem("img_eletivas",Eletivas.objects.all().values())
            return redirect(add_professor,tipo_de_user='professor')
    else:
        dados = {}
        dados['form'] = AddEletivaForm()
        dados['message'] = ''
        return render(request,'eletiva/addeletiva.html',dados)

def ver_eletiva(request,eletiva):
    dados = {}
    dados['alunos'] = Alunos.objects.filter(eletiva=eletiva).values()
    try:
        dados['professor'] = Professores.objects.filter(eletiva=eletiva)
    except:
        dados['message'] = 'Não professor responsável por essa eletiva'
    if len(dados['alunos']) == 0:
        dados['message'] = 'Não há alunos nesta eletiva'
    return  render(request,'eletiva/eletiva.html',dados)


def add_professor(request, tipo_de_user):
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
        return redirect(retornar_index)

    if request.method == 'POST':
        dados_do_ser_a_ser_adicionado = {}
        campos_universais = ['nome','email','password','descricao','eletiva']
        dados_do_ser_a_ser_adicionado['imagem'] = checar_imagem_existente(request.FILES.get('imagem'),'imagem_professores','cadastrar')
        for i in campos_universais:
            if tipo_de_user == 'professor' and i == 'descricao':
                dados_do_ser_a_ser_adicionado[f'{i}'] = ''
            elif tipo_de_user == 'tutor'and i == 'eletiva':
                dados_do_ser_a_ser_adicionado[f'{i}'] = ''
            else:
                dados_do_ser_a_ser_adicionado[f'{i}'] = request.POST.get(f'{i}')


        if tipo_de_user == 'professor':
            dados_do_ser_a_ser_adicionado['professor'] = True
            dados_do_ser_a_ser_adicionado['tutor'] = False
        elif tipo_de_user == 'tutor':
            dados_do_ser_a_ser_adicionado['tutor'] = True
            dados_do_ser_a_ser_adicionado['professor'] = False
        elif tipo_de_user == 'professor-tutor':
            dados_do_ser_a_ser_adicionado['tutor'] = True
            dados_do_ser_a_ser_adicionado['professor'] = True

        professor = Professores(eletiva=dados_do_ser_a_ser_adicionado['eletiva'],nome=dados_do_ser_a_ser_adicionado['nome'],email=dados_do_ser_a_ser_adicionado['email'],senha=dados_do_ser_a_ser_adicionado['password'],imagem=dados_do_ser_a_ser_adicionado['imagem'],professor=dados_do_ser_a_ser_adicionado['professor'],tutor=dados_do_ser_a_ser_adicionado['tutor'],descricao=dados_do_ser_a_ser_adicionado['descricao'])
        professor.save()
        return redirect(eletivas)
    else:
        dados={}
        if tipo_de_user != 'professor' and tipo_de_user != 'tutor' and tipo_de_user != 'professor-tutor':
            return redirect(retornar_index)
        
        dados['tipo_de_user'] = tipo_de_user
        dados['eletivas'] = Eletivas.objects
        dados['eletivas_para_for'] = Eletivas.objects.all().values()
        if tipo_de_user != 'tutor':
            for i in dados['eletivas_para_for']:
                p = Professores.objects.filter(eletiva=i['titulo'])
                if len(p) == 2:
                    dados['eletivas'] = dados['eletivas'].exclude(titulo=i['titulo'])
                    if len(dados['eletivas']) == 0:
                        dados['message'] = "Todas as eletivas possuem seus respectivos professores"
                        return redirect(retornar_index)
                elif len(p) == 0:
                    dados['eletivas'] = dados['eletivas'].all().values()
            
        return render(request,'professor/addprofessor.html',dados)

def add_aluno(request):
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
        return redirect(retornar_index)
    else:
        if request.method == 'POST':
            serie=request.POST.get('serie')
            nome=request.POST.get('nome')
            email=request.POST.get('email')
            senha=request.POST.get('senha')
            eletiva=request.POST.get('select')
            imagem=checar_imagem_existente(request.FILES.get('imagem'),'imagem_alunos',None)
            

            campos = [serie,nome,email,senha,eletiva]# checa se alguns dos valores acima e nulo
            for i in campos:
                
                if i == '':
                    dados={}
                    dados['eletivas'] = Eletivas.objects.all().values()
                    dados['message'] = 'A imagem de perfil é opcional porém os outros campos são obrigatórios'
                
                    return render(request,'aluno/addaluno.html',dados)
            aluno = Alunos(serie=serie,nome=nome,email=email,senha=senha,eletiva=eletiva, imagem=imagem)
            aluno.save()
            return redirect(ver_eletiva,eletiva=eletiva)
        else:
            dados={}
            dados['eletivas'] = Eletivas.objects.all().values()
            dados['message'] = 'A imagem de perfil é opcional'
            return render(request,'aluno/addaluno.html',dados)

def tutoria(request):
    dados=dados_universsais.copy()
    dados['pagina'] = 'tutoria'
    dados['tutores'] = Professores.objects.filter(tutor=True)
    return render(request,'principais/tutoria.html',dados)


# def addanuncio(request):
#     if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
#         return redirect(retornar_index)
#     else:
#         if request.method == 'POST':
#             form = AnuncioForm(request.POST, request.FILES)
#             if form.is_valid():
#                 anuncio = Anuncio(titulo=form.cleaned_data.get('titulo'),descricao=form.cleaned_data.get('descricao'),imagem=form.cleaned_data.get("imagem"),link=form.cleaned_data.get("link"))
#                 anuncio.save()
#                 return redirect(retornar_index)
            
#         else:
#             form = AnuncioForm()
#             return render(request, 'anuncio/addanuncio.html', {'form': form})
    

# def deletar_anuncio(request, anuncio_id):
#         if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'deletar') == True:
#             return redirect(retornar_index)
#         anuncio = Anuncio.objects.get(id=anuncio_id)
#         if request.method == 'POST':
#             sim = request.POST.get('sim')
#             if sim == 'on':
#                 anuncio.delete()
#             return redirect(retornar_index)
#         else:
#             return render (request, 'anuncio/deletaranuncio.html')

def editar_aviso(request,id):
    # if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
    #     return redirect(retornar_index)
    anuncio_a_ser_atualizado = Anuncio.objects.get(id=id)
    titulo_antigo = anuncio_a_ser_atualizado.titulo
    descricao_antiga = anuncio_a_ser_atualizado.descricao
    imagem_antiga = anuncio_a_ser_atualizado.imagem
    link_antigo = anuncio_a_ser_atualizado.link
    #Pega valores presentes no form
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        imagem = request.FILES.get('imagem')
        link = request.POST.get('link')
        #esta variavel contem todos os valores que forem inseridos  
        campos_novos = [titulo,descricao,imagem,link]
        #esta variavel contem todos os valores antigos do aviso
        campos_antigos = [titulo_antigo,descricao_antiga,imagem_antiga,link_antigo]
        tam = 0
        #for usado para checar se alguns dos anuncios e igual ao inserido na variavel campos novos
        for i in campos_novos:
            if tam == 0 and i != campos_antigos[tam]:
                anuncio_a_ser_atualizado.titulo = i
            elif tam == 1 and i != campos_antigos[tam]:
                anuncio_a_ser_atualizado.descricao = i
            elif tam == 2 and i != None:
                #checa se ja existe uma imagem na variavel
                imagem_final = checar_imagem_existente(imagem,'img_anuncio',None)
                anuncio_a_ser_atualizado.imagem = imagem_final
            elif tam == 3 and i != campos_antigos[tam]:
                anuncio_a_ser_atualizado.link = i
            tam += 1
        
        anuncio_a_ser_atualizado.save()
        excluir_imagem('img_anuncio',Anuncio.objects.all().values())

        return redirect(retornar_index)
    else:
        dados = {}
        dados['form'] = AnuncioForm()
        dados['titulo'] = anuncio_a_ser_atualizado.titulo
        dados['descricao'] = anuncio_a_ser_atualizado.descricao
        dados['imagem'] = anuncio_a_ser_atualizado.imagem
        dados['link'] = anuncio_a_ser_atualizado.link
        return render(request, 'anuncio/addanuncio.html', dados)

def update_eletiva(request,id):
    
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'atualizar') == True:
        return redirect(retornar_index)
    else:
        eletiva = get_object_or_404(Eletivas, id=id)
        eletiva_1 = str(eletiva.titulo)
        
        if request.method == 'POST':
            form = UpdateEletiva(request.POST,request.FILES,instance=eletiva)
            if form.is_valid():
                if form.cleaned_data.get('titulo') != eletiva_1:
                    professores = Professores.objects.filter(eletiva=eletiva_1)
                    alunos = Alunos.objects.filter(eletiva=eletiva_1)
                    if len(professores) != 0:
                        for professor in professores:
                            professor.eletiva = form.cleaned_data.get('titulo')
                            professor.save()
                       
                    if len(alunos) != 0:
                        for aluno in alunos:
                            aluno.eletiva = form.cleaned_data.get('titulo')
                            aluno.save()
        
                form.save()
                return redirect(eletivas)
            else:
                dados = {}
                dados['eletiva'] = Eletivas.objects.values().get(id=id)
                dados['modo'] = "update"
                dados['message'] = 'Dados inválidos'
                return render(request,'eletiva/addeletiva.html',dados)
        else:
            dados = dados_universsais.copy()
            dados['eletiva'] = Eletivas.objects.values().get(id=id)
            dados['modo'] = "update"
            dados['form'] = UpdateEletiva(instance=eletiva)
            return render(request,'eletiva/addeletiva.html',dados)
        
#função para mostrar os dados existentes pagina sobre
def sobre(request):
    dados = dados_universsais.copy()
    dados['pagina'] = 'sobre'
    return render(request,'principais/about.html',dados)
        
def deletar_com_ids(request,user,id):
        if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'deletar') == True:
            return redirect(retornar_index)
        
        dados = dados_universsais.copy()
        dados['lista_id'] = id.split(',')
        dados['tam_lista_id'] = len(dados['lista_id'])


        #if que verifica  se os id entre usuario e admin sao iguais e se for ira ser apresentada a menssagem de que o usuario nao pode se auto-deletar
        if dados['user'] == 'admin' and user == 'admin':
            id_do_user_logado = Admins.objects.get(nome=dados['nome_user_logado'],senha=dados['senha_user_logado']).id
            for i in dados['lista_id']:
                if int(i) == id_do_user_logado:
                    dados['message'] = 'Você não pode se auto deletar'
                    return redirect(update_or_delete,u_or_d='deletar', user=user)
        
        if request.method == 'POST':
            sim = request.POST.get('sim')
            nao = request.POST.get('nao')
            if sim == 'on' and nao != 'on':
                #ifs que deletam pelo id de acordo com o models escolhido: user=models='aluno,eletivas,admin ou professor' 
                if user == "aluno":
                    dados['model_user'] = Alunos.objects.all().values()
                    dados['diretorio_user'] = "imagem_alunos"
                    dados['user'] = 'alunos(s)'
                    for i in dados['lista_id']:
                        Alunos.objects.get(id=i).delete()

                elif user == "admin":
                    dados['model_user'] = Admins.objects.all().values()
                    dados['diretorio_user'] = "imagem_admins"
                    dados['user'] = 'admin(s)'
                    for i in dados['lista_id']:
                        Admins.objects.get(id=i).delete()

                elif user == "professor" or user == "tutor":
                    dados['model_user'] = Professores.objects.all().values()
                    dados['diretorio_user'] = "imagem_professores"
                    if user == 'tutor':
                        os_que_podem_ser_deletados = Professores.objects.filter(tutor=True)
                        dados['user'] = 'tutor(es)'
                        for i in dados['lista_id']:
                            user_da_vez = os_que_podem_ser_deletados.filter(id=i)
                            if len(user_da_vez) == 0:
                                dados['message'] = 'User não é um tutor'
                                return redirect(update_or_delete,u_or_d='deletar',user=user)
                            else:
                                Professores.objects.get(id=i).delete()
                    else:
                        dados['user'] = 'professor(es)'
                        os_que_podem_ser_deletados = Professores.objects.filter(professor=True)
                        for i in dados['lista_id']:
                            user_da_vez = os_que_podem_ser_deletados.filter(id=i)
                            if len(user_da_vez) == 0:
                                dados['message'] = 'User não é um professor'
                                return redirect(update_or_delete,u_or_d='deletar',user=user)
                            else:
                                Professores.objects.get(id=i).delete()
                elif user == "eletiva":
                    dados['model_user'] = Eletivas.objects.all().values()
                    dados['diretorio_user'] = "img_eletivas"
                    dados['user'] = 'eletiva(s)'
                    for i in dados['lista_id']:
                        eletiva_a_ser_deletada = Eletivas.objects.get(id=i) #.delete()
                        alunos_e_professores = [Professores.objects.filter(eletiva=eletiva_a_ser_deletada.titulo),Professores.objects.filter(eletiva=eletiva_a_ser_deletada.titulo)]
                        for i in alunos_e_professores:
                            for e in i:
                                e.eletiva = None
                                e.save()

                        eletiva_a_ser_deletada.delete()
                
                        

                            
            elif nao != "on" and sim != "on":

                dados['message'] = "selecione um dos valores"
                return redirect(deletar_com_ids, user=user,id=id)
            else:
                return redirect(update_or_delete,u_or_d='deletar',user=user)
            
            excluir_imagem(dados['diretorio_user'],dados['model_user'])
            if dados['diretorio_user'] == 'img_eletivas':
                excluir_imagem(f'{dados['diretorio_user']}/img_professores_eletiva',dados['model_user'])
            dados['message'] = f'Todo(s) o(s) {dados["tam_lista_id"]} {dados["user"]} deletado(s)'
            return redirect(update_or_delete,u_or_d='deletar',user=user)
        else:
            dados['message'] = ''
            if user == 'professor' or user == 'tutor':
                for i in dados['lista_id']:
                    professor_ou_tutor = Professores.objects.get(id=i)
                    user_da_vez = ''
        
                    if user == 'professor':
                        user_da_vez += 'tutor'
                        
                    else:
                        user_da_vez += 'professor'
                    if professor_ou_tutor.tutor == True and professor_ou_tutor.professor == True: 
                        dados['message'] = f'Dentre os selecionados está um {user_da_vez}, se apaga-lo como {user} também irá apaga-lo como {user_da_vez}'
                        break
            
            return render(request,'deletar/deletar_com_ids.html',dados)

def add_admin(request):
    if dados_universsais['user'] == 'admin':
        if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
            return redirect(retornar_index)
    
    if request.method == 'POST':
        nome = request.POST.get('nome').lower()
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        imagem = checar_imagem_existente(request.FILES.get('imagem'),'imagem_admins', None)
        

        #checkboxes= inputs do html
        checkboxes = ['deletar','atualizar','cadastrar']
        acoes_permitidas = ""
        for i in checkboxes:
            checkbox = request.POST.get(i)
            if checkbox == 'on':
                acoes_permitidas += f' {i}'
        novo_adm = Admins(nome=nome,senha=senha,email=email,acoes=acoes_permitidas,imagem=imagem)
        novo_adm.save()
        return redirect(retornar_index)
    else:
        return render(request,'acoes_principais/template_add.html')
def update_or_delete(request,u_or_d,user):
    if u_or_d != 'deletar' and u_or_d != 'update':
        return redirect(retornar_index)

    if u_or_d == 'update': 
        if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'atualizar') == True:
            return redirect(retornar_index)
    else:
        if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'deletar') == True:
            return redirect(retornar_index)
    dados = dados_universsais
    dados['tabela_user_passado_como_parametro'] = user

    dados['modo'] = f'{u_or_d}'
    if user.lower() == 'aluno':
        dados['usuarios'] = Alunos.objects.all().values()
    elif user.lower() == 'professor':
        dados['usuarios'] = Professores.objects.exclude(professor=False)
    elif user.lower() == 'admin':
        dados['usuarios'] = Admins.objects.all().values()
        if dados['user'] == 'admin' and u_or_d == 'deletar' : 
                dados['id_do_user_logado'] = Admins.objects.get(nome=dados['nome_user_logado'],senha=dados['senha_user_logado']).id
    elif user.lower() == 'eletiva':
            dados['usuarios'] = Eletivas.objects.all().values()
    elif user.lower() == 'tutor':
        dados['usuarios'] = Professores.objects.filter(tutor=True)
    else:
        dados['message'] = 'Usuário não identificado'
        return redirect(retornar_index)
    return render(request,f'{u_or_d}/{u_or_d}.html', dados)

def update_com_id(request,user,id):
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'atualizar') == True:
        return redirect(retornar_index)
    dados = {}
    user_a_ser_atualizado = []
    campos_atigos_do_user = []
    model = []

    #ifs para adcionar valores antigos do usuario
    if user == 'aluno':
        try:
            user_a_ser_atualizado.append(Alunos.objects.get(id=id))
        except:
            return redirect(update_or_delete,u_or_d='update', user=user)
        model.append(Alunos.objects.all().values())
        model.append("imagem_alunos")
        campos_atigos_do_user = [user_a_ser_atualizado[0].nome,user_a_ser_atualizado[0].email,user_a_ser_atualizado[0].senha,user_a_ser_atualizado[0].imagem,user_a_ser_atualizado[0].eletiva,user_a_ser_atualizado[0].serie]

    elif user == 'professor' or user == 'tutor':
        try:
            user_a_ser_atualizado.append(Professores.objects.get(id=id))
        except:
            dados['message'] = "User não encontrado"
            return redirect(update_or_delete,u_or_d='update', user=user)
        model.append(Professores.objects.all().values())
        model.append("imagem_professores")
        if user == 'tutor':
            campos_atigos_do_user = [user_a_ser_atualizado[0].nome,user_a_ser_atualizado[0].email,user_a_ser_atualizado[0].descricao]
        else:
            campos_atigos_do_user = [user_a_ser_atualizado[0].nome,user_a_ser_atualizado[0].email,user_a_ser_atualizado[0].senha,user_a_ser_atualizado[0].imagem,user_a_ser_atualizado[0].eletiva]
    elif user == 'eletiva':
        try:
            user_a_ser_atualizado.append(Eletivas.objects.get(id=id))
        except:
            return redirect(update_or_delete,u_or_d='update', user=user)
        model.append(Eletivas.objects.all().values())
        model.append("img_eletivas")
        campos_atigos_do_user = [user_a_ser_atualizado[0].titulo,user_a_ser_atualizado[0].descricao,user_a_ser_atualizado[0].imagem,user_a_ser_atualizado[0].img_professores_eletiva,user_a_ser_atualizado[0].link]
    elif user == 'admin':
        try:
            admin_a_ser_atualizado = Admins.objects.get(id=id)
        except:
            return redirect(update_or_delete,u_or_d='update', user=user)
        if admin_a_ser_atualizado.nome == request.session['nome_user_logado'] and 'atualizar' in request.session['lista_de_acoes'] :
            dados['message'] = "Você não pode se auto atualizar"
            return redirect(update_or_delete,u_or_d='update', user=user)
        model.append(Admins.objects.all().values())
        model.append("imagem_admins")
        user_a_ser_atualizado.append(admin_a_ser_atualizado)
        campos_atigos_do_user = [user_a_ser_atualizado[0].nome,user_a_ser_atualizado[0].email,user_a_ser_atualizado[0].senha,user_a_ser_atualizado[0].imagem,user_a_ser_atualizado[0].acoes]
 
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        imagem = request.FILES.get('imagem')
        pergunta_imagem = request.POST.get('pergunta_imagem')
        pergunta_imagem_professores = request.POST.get('pergunta_imagem_professores')
            
        campos_atualizados_do_user = []
        #ifs que pegamm valores atuais dos usuarios
        if user == 'aluno' or user == 'professor':
            eletiva = request.POST.get('eletiva')
            campos_atualizados_do_user = [nome,email,senha,imagem,eletiva]
            if user == 'aluno':
                serie = request.POST.get('serie')
                campos_atualizados_do_user = [nome,email,senha,imagem,eletiva,serie]
        elif user == 'tutor':
            descricao = request.POST.get('descricao')
            campos_atualizados_do_user = [nome,email,senha,imagem,descricao]
        elif user == 'eletiva':
            titulo = request.POST.get('titulo')
            link = request.POST.get('link')
            descricao = request.POST.get('descricao')
            img_professores = request.FILES.get('img_professores')
            campos_atualizados_do_user = [titulo,descricao,imagem,img_professores,link]
        elif user == 'admin':
            checkboxes = ['deletar','atualizar','cadastrar']
            acoes_permitidas = ""
            for i in checkboxes:
                checkbox = request.POST.get(i)
                if checkbox == 'on':
                    acoes_permitidas += f' {i}'
            
            campos_atualizados_do_user = [nome,email,senha,imagem,acoes_permitidas]
        

        tam = 0
        
        #for que percorre os valores do usuario e checa se o nome atual do usuario e uigual ao antigo e se for diferente altera ele 
        for i in campos_atualizados_do_user:
            if i != campos_atigos_do_user[0]:
                if tam == 0:
                    if user == 'eletiva':
                        professores = Professores.objects.filter(eletiva=str(user_a_ser_atualizado[0].titulo))
                        alunos = Alunos.objects.filter(eletiva=str(user_a_ser_atualizado[0].titulo))
                        if len(professores) != 0:
                            for e in professores:
                                e.eletiva = i
                                e.save()

                        if len(alunos) != 0:
                            for e in alunos:
                                e.eletiva = i
                                e.save()
                        user_a_ser_atualizado[0].titulo = i
                    else:
                        user_a_ser_atualizado[0].nome = i
                elif tam == 1 and user != 'eletiva':
                    user_a_ser_atualizado[0].email = i
                elif tam == 2 and user != 'eletiva':
                    user_a_ser_atualizado[0].senha = i
                elif tam == 3 and user != 'eletiva' or tam == 2 and user == 'eletiva' :
                    if imagem != None and pergunta_imagem == 'on' or imagem == None and pergunta_imagem == 'on':
                        user_a_ser_atualizado[0].imagem = checar_imagem_existente(None,model[1],'atualizar')
                    elif imagem != None and pergunta_imagem == None:
                        user_a_ser_atualizado[0].imagem = checar_imagem_existente(imagem,model[1],'atualizar')
                elif tam == 3 and user == 'eletiva':
                    if img_professores != None and pergunta_imagem_professores == 'on' or img_professores == None and pergunta_imagem_professores == 'on':
                        user_a_ser_atualizado[0].img_professores_eletiva = checar_imagem_existente(None,f'img_eletivas/img_professores_eletiva','atualizar')
                    elif img_professores != None and pergunta_imagem_professores == None:
                        user_a_ser_atualizado[0].img_professores_eletiva = checar_imagem_existente(img_professores,f'img_eletivas/img_professores_eletiva','atualizar')
                  
                elif tam == 4 and user != 'admin' and user != 'tutor':
                    user_a_ser_atualizado[0].eletiva = i
                elif tam == 4 and user == 'admin':
                    user_a_ser_atualizado[0].acoes = i
                elif tam == 4 and user == 'tutor' or user == 'eletiva' and tam == 1:
                    user_a_ser_atualizado[0].descricao = i
                elif tam == 5:
                    user_a_ser_atualizado[0].serie = i
            tam += 1
        user_a_ser_atualizado[0].save()
        
        if user == 'eletiva':
            excluir_imagem(f'{model[1]}/img_professores_eletiva',model[0])
        excluir_imagem(model[1],model[0])
        return redirect(update_or_delete,u_or_d='update',user=user)

        


    else:
        
        dados['user'] = user
        dados['tabela'] = user_a_ser_atualizado[0]
        dados['eletivas'] = Eletivas.objects.all().values()
        dados['message'] = ''
        if user == 'admin':
            acoes_lista = campos_atigos_do_user[4].split()
            for i in acoes_lista:
                dados[f'{i}'] = 'checked'
        
        return render(request, 'update/update_com_id.html', dados)


