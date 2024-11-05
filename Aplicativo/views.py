from django.shortcuts import render,redirect
from .forms import LoginForm,AddEletivaForm, AnuncioForm
from django.contrib.auth import login, authenticate, logout
from .models import *
import os
from PIL import Image
#acabar de fazer os 'link_antigo' templates adicionar
#pip freeze > requiriments.txt
menssagem_var = {'mensagem':""}

#esta variável receberá o valor que eu precisarei em todas as funções, ela server para eu não ter que ficar
#repetindo linhas de código. Em quase todas as funções a variável 'dados' hospedará o valor dela.
dados_universsais = {}

def ver_se_a_pagina_pode_funcionar(pagina,dados):
    #false: não saía
    #true: saía
    #tente pegar os valores do object
    try:
        paginaModels = PaginasUtilizaveis.objects.values().get(id=1)
    #se não conseguir é porque não existe, então crie-o
    except:
        p1 = PaginasUtilizaveis(tutoria=True,eletiva=True,index=True,sobre=True)
        p1.save()
        return False 
    #pegua o valor referente a página passada como parâmetro, se for diferente de true é porque ela não pode ser utilizada 
    if paginaModels[f'{pagina}'] != True:
        dados['message'] = menssagem_var['mensagem']
        menssagem_var['mensagem'] = ""
        return True
    else:
        return False
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
    try:
        #variável que guarda todas imagens da pasta media
        imagens_da_pasta_solicitada = os.listdir(f'{os.getcwd()}/media/{dir}')
    except:
        return
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
    if user == None or acao == 'definirpaginas' and user != 'ADMIN':
        menssagem_var['mensagem'] = "Você não pode realizar a ação requisitada!"
        return True
    #caso o usuário for um admin tem que ser verificado se ele pode realizar a ação requisitada
    elif user == 'admin':
        #verifica se a ação existe, se existir o fluxo do código não é alterado, se não existir retorna True
        #ou seja: o usuário não pode realizar a ação pois ação não existe
        if acao in request.session['lista_de_acoes']:
            return False
        else: 
            menssagem_var['mensagem'] = "Você não pode realizar a ação requisitada!"
            return True
    #caso o user seja o ADMIN ele poderá fazer qualquer coisa independentemente da ação requisitada
    elif user == 'ADMIN':
        return False
    else:
        #se nenhuma dos ifs anteriores der certo então retorne True
        menssagem_var['mensagem'] = "Você não pode realizar a ação requisitada!"
        return True
def definir_user(request):
       #if que verifica se o ADMIN já estava logado
    if request.user.is_authenticated:
        request.session['user'] = 'ADMIN'
        request.session['nome_user_logado'] = ''
        request.session['senha_user_logado'] = ''
 
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
        #caso o user logado seja um admin precisarei da senha e do nome dele, para impedir que ele se auto atualize ou delete
        dados['nome_user_logado'] = request.session['nome_user_logado']
        dados['senha_user_logado'] = request.session['senha_user_logado']
        #caso o usuário for um admin então eu preciso de uma variável com todas as ações que ele pode realizar
        if dados['user'] == 'admin':
            dados['lista_de_acoes'] = request.session['lista_de_acoes']
    #atualizando a variável dos dados universsais para que eu possa acessar os valores adicionados de outras fuções
    dados_universsais.update(dados)
    return dados
def para_onde_vou(request,link_antigo):
    if "eletivas" in link_antigo:
        return redirect(eletivas)
    elif "sobre" in link_antigo:
        return redirect(sobre)
    elif "tutoria" in link_antigo:
        return redirect(tutoria)
    elif "definir-paginas" in link_antigo:
        return redirect(definir_paginas_utilizaveis)
    elif  link_antigo == "/":
        return redirect(retornar_index)
    link_lista = link_antigo.split("/")
    if link_lista[2] == 'update_or_delete':
        return redirect(update_or_delete,u_or_d=link_lista[3],user_a_ser_atualizado_arg=link_lista[4])
    elif link_lista[2] == 'deletar' or link_lista[2] == 'atualizar':
        return redirect(deletar_com_ids,user_a_ser_atualizado_arg=link_lista[3],id=link_lista[4])
    
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

#nesta função é feito o login dos usuários 
def login_viwes(request):
    try:
        request.session['user']
    except:
        request.session['user'] = None
    #esse if verifica se já tem um usuário logado, se tiver é necessário que deslogue para logar de novo
    if request.session['user'] == 'ADMIN'or request.session['user'] != None:
        return redirect(retornar_index)
    
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
    ids = CarrosselProfessores.objects.get(id=1).ids.split(',')
    dados['carrossel'] = [Professores.objects.filter(id=int(ids[0])).values(),Professores.objects.filter(id=int(ids[1])).values(),Professores.objects.filter(id=int(ids[2])).values()]
    for i in dad
    #####################################
    return render(request,'eletiva/eletivas.html',dados)

#função que desloga o usuário
def logout_viwes(request):
    if request.method == "POST":
        user = request.session['user'] 
        #o admin supremo(ADMIN) é o único que foi criado como um user no django e por isso ele recebe um 
        #tratamento diferente dos demais, a função logout() é própria do Django ela server para deslogar o user que esta logado
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
        menssagem_var['mensagem'] = "Deslogado com sucesso!"
        link = request.POST.get('link_antigo')
        print(link)
        return para_onde_vou(request,link)

#função que adiciona as eletivas
def add_eletivas(request):
    #chama a função que verifica se o usuário está apto ou não à adicionar eletivas ou não
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
        return redirect(retornar_index)
    
    if request.method == 'POST':
        #chamando o form 
        form = AddEletivaForm(request.POST, request.FILES)
        if form.is_valid():
            #variável que armazena o nome da eletiva
            eletiva = form.cleaned_data.get('titulo')
            #variável que armazena a imagem de fundo da eletiva
            imagem = checar_imagem_existente(form.cleaned_data.get("imagem"),"img_eletivas",None)
            #variável que armazena a imagem dos professores da eletiva. Ele recebe o "request.FILES.get" porque  este campo não esta presente no form do django
            imagem_p = checar_imagem_existente(request.FILES.get("imagem_p"),"img_eletivas/img_professores_eletiva",None)
            #criando a nova eletiva
            new = Eletivas(titulo=eletiva,descricao=form.cleaned_data.get('descricao'),imagem=imagem,img_professores_eletiva=imagem_p,link=form.cleaned_data.get("link"))
            #salvando-a
            new.save()
            #redirecionando para a função que adiciona o professor responsável pela eletiva
            excluir_imagem("img_eletivas",Eletivas.objects.all().values())
            menssagem_var['mensagem'] = "Eletiva Adicionada!"
            return redirect(add_professor,tipo_de_user='professor')
    else:
        dados = {}
        #variável que retorna o form para o html
        dados['form'] = AddEletivaForm()
        dados['message'] = ''
        return render(request,'eletiva/addeletiva.html',dados)

#função que adiciona os professores e/ou tutores
#tipo_de_user: tipo do user a ser adicionado(professor/tutor)
def add_professor(request, tipo_de_user):
    #chama a função que verifica se o usuário está apto ou não à adicionar professores ou não
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
        return redirect(retornar_index)

    if request.method == 'POST':
        dados_do_ser_a_ser_adicionado = {}
        #esta variável armazena os campos que não possuem valores booleanos
        campos_universais = ['nome','email','password','descricao','eletiva']
        #armazena a nova imagem do professor/tutor 
        dados_do_ser_a_ser_adicionado['imagem'] = checar_imagem_existente(request.FILES.get('imagem'),'imagem_professores','cadastrar')
        #percorre os campos para adiciona-los a variável 'dados_do_ser_a_ser_adicionado'
        for i in campos_universais:
            #se o user a ser adicionado for um professor então eu não preciso de descrição
            if tipo_de_user == 'professor' and i == 'descricao':
                dados_do_ser_a_ser_adicionado[f'{i}'] = ''
            #se o user a ser adicionado for um tutor então eu não preciso de eletiva
            elif tipo_de_user == 'tutor'and i == 'eletiva':
                dados_do_ser_a_ser_adicionado[f'{i}'] = ''
            #do contrário adicione os valores
            else:
                dados_do_ser_a_ser_adicionado[f'{i}'] = request.POST.get(f'{i}')

        #no models referente aos professores e tutores tem 2 campos booleano que dizem se o indivíduo é um professor, tutor ou ambos
        #se for professor, o campo do professor no models receberá True e o de tutor receberá False ou vice-versa
        if tipo_de_user == 'professor':
            dados_do_ser_a_ser_adicionado['professor'] = True
            dados_do_ser_a_ser_adicionado['tutor'] = False
        elif tipo_de_user == 'tutor':
            dados_do_ser_a_ser_adicionado['tutor'] = True
            dados_do_ser_a_ser_adicionado['professor'] = False
        elif tipo_de_user == 'professor-tutor':
            dados_do_ser_a_ser_adicionado['tutor'] = True
            dados_do_ser_a_ser_adicionado['professor'] = True
        #criando um novo professor ou tutor
        professor = Professores(eletiva=dados_do_ser_a_ser_adicionado['eletiva'],nome=dados_do_ser_a_ser_adicionado['nome'],email=dados_do_ser_a_ser_adicionado['email'],senha=dados_do_ser_a_ser_adicionado['password'],imagem=dados_do_ser_a_ser_adicionado['imagem'],professor=dados_do_ser_a_ser_adicionado['professor'],tutor=dados_do_ser_a_ser_adicionado['tutor'],descricao=dados_do_ser_a_ser_adicionado['descricao'])
        #salvando-o
        professor.save()
        if tipo_de_user == 'tutor':
            menssagem_var['mensagem'] = "Tutor adicionado!"
            return redirect(tutoria)
        elif tipo_de_user == 'professor-tutor':
            menssagem_var['mensagem'] = "Professor/tutor adicionado!"
            return redirect(eletivas)
        else:
            menssagem_var['mensagem'] = "Professor adicionado!"
            return redirect(eletivas)
    else:
        dados={}
        try:
            dados['message'] = menssagem_var['mensagem']
            menssagem_var['mensagem'] = ""
        except:
            dados['message'] = ''
        #como essa função só adiciona professor ou tutor, se o 'tipo_de_user' for difente não poderá ser adicionado
        if tipo_de_user != 'professor' and tipo_de_user != 'tutor' and tipo_de_user != 'professor-tutor':
            return redirect(retornar_index)
        #como há campos pertencentes ao professor que são diferentes dos campos de um tutor
        #nesta variável eu retorno o tipo do user, e lá no html,através de um if só será mostrado os campos referentes ao user a ser adicionado
        dados['tipo_de_user'] = tipo_de_user
        #recebe as eletivas: poderei executar o 'exclude'
        dados['eletivas'] = Eletivas.objects
         #recebe as eletivas: não poderei executar o 'exclude', porém, percorrerei-a para verificar se há eletivas sem professores
        dados['eletivas_para_for'] = Eletivas.objects.all().values()
        if len(dados['eletivas_para_for']) == 0:
            return redirect(retornar_index)
        if tipo_de_user != 'tutor':
            #este for verifica se tem alguma eletiva sem professor
            for i in dados['eletivas_para_for']:
                p = Professores.objects.filter(eletiva=i['titulo'])
                #se o tamanho da variável 'p' é igual a 2, é porque a eletiva está completa no quesito professor
                if len(p) == 2:
                    #estão exclua a respectiva eletiva da veriável 'dados['eletivas']'
                    dados['eletivas'] = dados['eletivas'].exclude(titulo=i['titulo'])
                    #se o tamanho da variável "dados['eletivas']" for igual a zero é porque não tem eletiva para ser adicionado um professor responsável
                    #logo, o professor não poderá ser adicionado
                    if len(dados['eletivas']) == 0:
                        menssagem_var['mensagem'] = "Todas as eletivas já possuem seus respectivos professores"
                        return redirect(eletivas)
                # elif len(p) == 0:
                #     dados['eletivas'] = dados['eletivas'].all().values()
        #como eu tinha que executar o 'exclude' eu não podia obter os 'values' do models 'Eletivas', porém, agora posso
        dados['eletivas'] = dados['eletivas'].values()
        return render(request,'professor/addprofessor.html',dados)
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
#função que edita e se ele não existir cria o aviso
def editar_aviso(request,id):
    #verificando se a página pode funcionar
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
        return redirect(retornar_index)
    #como são só 2 avisos então não faz sentido o id passado na url ser maior que 2
    if id <= 2 and id > 0:
        #tente pegar o aviso, se não der é porque ele não existe, então crie-o(são criados os avisos de id 1 e 2)
        try:
            anuncio_a_ser_atualizado = Anuncio.objects.get(id=id)
        except:
            #número de avisos adicionados
            anuncios = 1
            #enquato 'anuncios' for menor ou igual a 2(limite de avisos)
            while anuncios <= 2:
                #crie avisos com quaisquer valores(exceto o id)
                anuncio_a_ser_cadastrado = Anuncio(id=anuncios,titulo='titulo',descricao='descricao',imagem=checar_imagem_existente(None,'img_anuncio',None),link='https://www.google.com.br')
                #salve-os
                anuncio_a_ser_cadastrado.save()
                #atribua 1 à variável 'anuncios', pois 1 aviso foi adicionado 
                anuncios += 1
            #pegue o aviso com o respectivo id
            anuncio_a_ser_atualizado = Anuncio.objects.get(id=id)
        #todos os valores antigos do aviso
        titulo_antigo = anuncio_a_ser_atualizado.titulo
        descricao_antiga = anuncio_a_ser_atualizado.descricao
        imagem_antiga = anuncio_a_ser_atualizado.imagem
        link_antigo = anuncio_a_ser_atualizado.link
        #Pega valores presentes no form
        if request.method == 'POST':
            #todos os novos valores do aviso
            titulo = request.POST.get('titulo')
            descricao = request.POST.get('descricao')
            imagem = request.FILES.get('imagem')
            link = request.POST.get('link')
            #esta variavel contem todos os valores que forem inseridos  
            campos_novos = [titulo,descricao,imagem,link]
            #esta variavel contem todos os valores antigos do aviso
            campos_antigos = [titulo_antigo,descricao_antiga,imagem_antiga,link_antigo]
            #variável que representa em qual campo o loop for esta, ex: 0=titulo_antigo,1=descricao_antiga...
            tam = 0
            #for usado para checar se algum dos campos do anuncio e igual ao inserido na variavel campos novos
            for i in campos_novos:
                #somente se for diferente adicione. O campo da imagem é só se for diferente de None
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
            #salvando as alterações efetuadas
            anuncio_a_ser_atualizado.save()
            #chamando a função que exclui a imagem se ela não esta mais sendo usada
            excluir_imagem('img_anuncio',Anuncio.objects.all().values())
            return redirect(retornar_index)
        else:
            dados = {}
            #MODIFICAR AQUI#
            dados['form'] = AnuncioForm()
            dados['titulo'] = anuncio_a_ser_atualizado.titulo
            dados['descricao'] = anuncio_a_ser_atualizado.descricao
            dados['imagem'] = anuncio_a_ser_atualizado.imagem
            dados['link'] = anuncio_a_ser_atualizado.link
            return render(request, 'anuncio/addanuncio.html', dados)
    #se o id for diferente de 1 ou 2 saía daqui
    else:
        return redirect(retornar_index)
#função que atualiza a eletiva
#excluir esta função

        
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
    return render(request,'principais/about.html',dados)
        
def deletar_com_ids(request,user_a_ser_atualizado_arg,id):
        #verificando se o usuário pode deletar
        if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'deletar') == True:
            return redirect(retornar_index)
        dados = dados_universsais.copy()
        #como os ids passados na url são strings, esta linha passa-os para uma lista
        dados['lista_id'] = id.split(',')
        #variável que recebe o tamanho da lista de ids
        dados['tam_lista_id'] = len(dados['lista_id'])
       #se o user a ser deletado for um 'admin' e o user logado for o mesmo admin ele não poderá se auto deletar
        if dados['user'] == 'admin' and user_a_ser_atualizado_arg == 'admin':
            #pego o id referente ao admin logado
            id_do_user_logado = Admins.objects.get(nome=dados['nome_user_logado'],senha=dados['senha_user_logado']).id
            #loop para percorrer os ids
            for i in dados['lista_id']:
                #se o id passado como parâmetro for igual ao id do user logado, impessa que o delete aconteça
                if int(i) == id_do_user_logado:
                    menssagem_var['mensagem'] = "Você não pode se auto deletar!"
                    return redirect(update_or_delete,u_or_d='deletar', user_a_ser_atualizado_arg=user_a_ser_atualizado_arg)
        
        if request.method == 'POST':
            #pegando os valores dos inputs do html
            sim = request.POST.get('sim')
            nao = request.POST.get('nao')
            #if para deletar
            if sim == 'on' and nao != 'on':
                if user_a_ser_atualizado_arg == "admin":
                    dados['model_user'] = Admins.objects.all().values()
                    dados['diretorio_user'] = "imagem_admins"
                    dados['user'] = 'admin(s)'
                    for i in dados['lista_id']:
                        try:
                            Admins.objects.get(id=i).delete()
                        except:
                            return redirect(update_or_delete,u_or_d='deletar',user_a_ser_atualizado_arg=user_a_ser_atualizado_arg)
                #se o user_a_ser_atualizado_arg for um professor ou tutor
                elif user_a_ser_atualizado_arg == 'oferecimento':
                    if dados['user'] != 'ADMIN':
                        menssagem_var['mensagem'] = 'somente o ADMIN(diretor) pode deletar o oferecimentos'
                        return redirect(retornar_index)
                    else:
                        id_a_ser_deletado = dados['lista_id'][0]
                        dados['model_user'] = OqueTemosaOferecer.objects.all().values()
                        dados['diretorio_user'] = "img_OqueTemosaOferecer"
                        try:
                            OqueTemosaOferecer.objects.get(id=id_a_ser_deletado).delete()
                            excluir_imagem('img_OqueTemosaOferecer',OqueTemosaOferecer.objects.all().values())
                            menssagem_var['mensagem'] = 'O oferecimento foi deletado'
                            return redirect(retornar_index)
                        except:
                            menssagem_var['mensagem'] = 'Id não encontrado'
                            return redirect(retornar_index)
                elif user_a_ser_atualizado_arg == "professor" or user_a_ser_atualizado_arg == "tutor":
                    dados['model_user'] = Professores.objects.all().values()
                    dados['diretorio_user'] = "imagem_professores"
                    #se o user for tutor
                    if user_a_ser_atualizado_arg == 'tutor':
                        #variável que recebe somente os objects que são tutores
                        os_que_podem_ser_deletados = Professores.objects.filter(tutor=True)
                        dados['user'] = 'tutor(es)'
                        #loop que percorre a lista de ids
                        for i in dados['lista_id']:
                            #recebe o user a ser deletado
                            user_da_vez = os_que_podem_ser_deletados.filter(id=i)
                            #se o tamanho da variável 'user_da_vez' for igual a 0 é poque o id passado não é de um tutor
                            #logo, ele não poderá ser deletado
                            if len(user_da_vez) == 0:
                                menssagem_var['mensagem'] = "User não é um tutor"
                                return redirect(update_or_delete,u_or_d='deletar',user_a_ser_atualizado_arg=user_a_ser_atualizado_arg)
                            else:
                                 #tente pegar o object de id = i e delete-o
                                try:
                                    Professores.objects.get(id=i).delete()
                                except:
                                     #se não conseguir saía daqui
                                    return redirect(update_or_delete,u_or_d='deletar',user_a_ser_atualizado_arg=user_a_ser_atualizado_arg)
                    else:
                        dados['user'] = 'professor(es)'
                        #variável que recebe somente os objects que são professores
                        os_que_podem_ser_deletados = Professores.objects.filter(professor=True)
                        for i in dados['lista_id']:
                         #recebe o user a ser deletado
                            user_da_vez = os_que_podem_ser_deletados.filter(id=i)
                             #se o tamanho da variável 'user_da_vez' for igual a 0 é poque o id passado não é de um tutor
                            #logo, ele não poderá ser deletado
                            if len(user_da_vez) == 0:
                                menssagem_var['mensagem'] = "User não é um professor"
                                return redirect(update_or_delete,u_or_d='deletar',user_a_ser_atualizado_arg=user_a_ser_atualizado_arg)
                            else:
                                try:
                                    Professores.objects.get(id=i).delete()
                                except:
                                    return redirect(update_or_delete,u_or_d='deletar',user_a_ser_atualizado_arg=user_a_ser_atualizado_arg)
                #se o user passado como parâmetro for igual a eletiva
                elif user_a_ser_atualizado_arg == "eletiva":
                    dados['model_user'] = Eletivas.objects.all().values()
                    dados['diretorio_user'] = "img_eletivas"
                    dados['user'] = 'eletiva(s)'
                    for i in dados['lista_id']:
                        try:
                            eletiva_a_ser_deletada = Eletivas.objects.get(id=i) #.delete()
                        except:
                            return redirect(update_or_delete,u_or_d='deletar',user_a_ser_atualizado_arg=user_a_ser_atualizado_arg)
                      #como têm professores e alunos nas eletivas, para apaga-la será necessário retira-los desta. Esta variável
                        #recebe uma lista com professores e alunos da referente eletiva
                        alunos_e_professores = [Professores.objects.filter(eletiva=eletiva_a_ser_deletada.titulo),Professores.objects.filter(eletiva=eletiva_a_ser_deletada.titulo)]
                        #loop para percorrer a variável 'alunos_e_professores'
                        for i in alunos_e_professores:
                            #loop para percorrer a variável da variável 'alunos_e_professores'(professores ou aluno) 
                            for e in i:
                                #definindo o campo eletiva deles como None
                                e.eletiva = None
                                #salvando
                                e.save() 
                        #deletendo a eletiva
                        eletiva_a_ser_deletada.delete()
            #se ambos valores forem diferentes de 'on' é porque nenhum dos inputs foram marcados, por conguinte, saía daqui
            elif nao != "on" and sim != "on":
                menssagem_var['mensagem'] = "selecione um dos valores"
                return redirect(deletar_com_ids, user_a_ser_atualizado_arg=user_a_ser_atualizado_arg,id=id)
            else:
                return redirect(update_or_delete,u_or_d='deletar',user_a_ser_atualizado_arg=user_a_ser_atualizado_arg)
            
            excluir_imagem(dados['diretorio_user'],dados['model_user'])
            #como a eletiva tem dois campos que requerem imagens, é necessário que a função 'excluir_imagem' seja chamada novamente, 
            #agora excluindo as imagens dos professores
            if dados['diretorio_user'] == 'img_eletivas':
               excluir_imagem(f"{dados['diretorio_user']}/img_professores_eletiva", dados['model_user'])
            menssagem_var['mensagem'] = f'Todo(s) o(s) {dados["tam_lista_id"]} {dados["user"]} deletado(s)'
            return redirect(update_or_delete,u_or_d='deletar',user_a_ser_atualizado_arg=user_a_ser_atualizado_arg)
        else:
            dados['message'] = ""
            #esse if checa se o professor também é um tutor ou vice-versa e retorna uma mensagem informando ao usuário
            if user_a_ser_atualizado_arg == 'professor' or user_a_ser_atualizado_arg == 'tutor':
                #loop que percorre a lista com ids
                for i in dados['lista_id']:
                    #pega o professor/tutor
                    try:   
                        professor_ou_tutor = Professores.objects.get(id=i)
                    except:
                        return redirect(update_or_delete,u_or_d='deletar',user_a_ser_atualizado_arg=user_a_ser_atualizado_arg)
                    #variável que recebe o valor contrário ao user passado como parâmetro
                    user_da_vez = ''
                    if user_a_ser_atualizado_arg == 'professor':
                        user_da_vez += 'tutor'
                    else:
                        user_da_vez += 'professor'
                    #se ambos campos 'tutor' e 'professor' forem True é porque ele é professor e tutor, logo, retorne uma mensagem
                    if professor_ou_tutor.tutor == True and professor_ou_tutor.professor == True and menssagem_var['mensagem'] != "selecione um dos valores": 
                        menssagem_var['mensagem'] = f'Dentre os selecionados está um {user_da_vez}, se apaga-lo como {user_a_ser_atualizado_arg} também irá apaga-lo como {user_da_vez}'
                        break
            dados['message'] = menssagem_var['mensagem']
            return render(request,'deletar/deletar_com_ids.html',dados)
#função que adiciona o admin
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
        #variável que recebe em forma de string as ações que o admin pode realizar
        acoes_permitidas = ""
        #loop que percorre os checkboxes e se algun deles estiver marcado então irá adiciona-lo na variável acima
        for i in checkboxes:
            checkbox = request.POST.get(i)
            if checkbox == 'on':
                acoes_permitidas += f' {i}'
        #criando o novo admin 
        novo_adm = Admins(nome=nome,senha=senha,email=email,acoes=acoes_permitidas,imagem=imagem)
        novo_adm.save()
        #retornado a respectiva menssagem
        menssagem_var['menssagem'] = "Admin adicionado com sucesso!"
        return redirect(retornar_index)
    else:
        return render(request,'acoes_principais/template_add.html')
#função que direciona o usuário para a página de Deletar ou Atualizar, com respectivas variáveis necessárias
def update_or_delete(request,u_or_d,user_a_ser_atualizado_arg):
    #caso a variável passada na url seja diferente das ações que esta função pode realizar
    if u_or_d != 'deletar' and u_or_d != 'atualizar':
        return redirect(retornar_index)

    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,f'{u_or_d}') == True:
        return redirect(retornar_index)
   
    dados = dados_universsais.copy()
    #esta variável nos dirá qual tabela deverá ser usada no html
    dados['tabela_user_passado_como_parametro'] = user_a_ser_atualizado_arg
    #dirá se no html usará os templates de deletar ou od de atualizar 
    dados['modo'] = f'{u_or_d}'
    #caso seja professor
    if user_a_ser_atualizado_arg.lower() == 'professor':
        dados['usuarios'] = Professores.objects.exclude(professor=False)
    #caso seja admin
    elif user_a_ser_atualizado_arg.lower() == 'admin':
        dados['usuarios'] = Admins.objects.all().values()
        #para impedir que o usuário não se auto-delete ou auto-atualize eu pego o id do user que está logado
        #e mais a frente compararei este id com os ids selecionados pelo usuário
        if dados['user'] == 'admin' and u_or_d == 'deletar' : 
                dados['id_do_user_logado'] = Admins.objects.get(nome=dados['nome_user_logado'],senha=dados['senha_user_logado']).id
    #caso seja eletiva
    elif user_a_ser_atualizado_arg.lower() == 'eletiva':
            dados['usuarios'] = Eletivas.objects.all().values()
    #caso seja tutor
    elif user_a_ser_atualizado_arg.lower() == 'tutor':
        dados['usuarios'] = Professores.objects.filter(tutor=True)
    #caso seja professor/tutor
    elif user_a_ser_atualizado_arg.lower() == 'professor-tutor':
        dados['usuarios'] = Professores.objects.filter(professor=True,tutor=True)
    #caso seja nenhum dos acima
    else:
        menssagem_var['mensagem'] = "Usuário não identificado"
        return redirect(retornar_index)
    #pegando a menssagem
    dados['message'] = menssagem_var['mensagem'] 
    #apagando-a da variável "menssagem_var", isso significa que ela já foi usada
    menssagem_var['mensagem'] = ""
    #retornando para a respectiva página
    return render(request,f'{u_or_d}/{u_or_d}.html', dados)
#função que atualiza 
def update_com_id(request,user_a_ser_atualizado_arg,id):
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'atualizar') == True:
        return redirect(retornar_index)
    dados = {}
    #variável que recebe o user a ser atualizar, está como lista pois assim eu posso editá-lo 
    user_a_ser_atualizado = []
    #variável que receberá todos os campos antigos do usuário a ser atualizado
    campos_atigos_do_user = []
    #recebe o miodel no qual o user esta situado e a pasta osta esta localizada sua imagem de perfil
    model = []
    if user_a_ser_atualizado_arg == 'professor' or user_a_ser_atualizado_arg == 'tutor' or user_a_ser_atualizado_arg == 'professor-tutor':
        #tente adicionar o user
        try:
            user_a_ser_atualizado.append(Professores.objects.get(id=id))
        #se não conseguir saía daqui
        except:
            menssagem_var['mensagem'] = "User não encontrado"
            return redirect(update_or_delete,u_or_d='atualizar', user_a_ser_atualizado_arg=user_a_ser_atualizado_arg)
        if user_a_ser_atualizado[0].tutor == True and user_a_ser_atualizado[0].professor == True and user_a_ser_atualizado_arg != 'professor-tutor':
            return redirect(update_com_id, user_a_ser_atualizado_arg='professor-tutor',id=id)
        #já que chegou até aqui é porque está dando certo
        #entã, adicione à variável "model" o models do usuário e a pasta
        model.append(Professores.objects.all().values())
        model.append("imagem_professores")
        #como tutores, professores e professores-tutores têm campos diferentes, estes ifs adicionam somente os campos necessários 
        if user_a_ser_atualizado_arg == 'tutor':
            campos_atigos_do_user = [user_a_ser_atualizado[0].nome,user_a_ser_atualizado[0].email,user_a_ser_atualizado[0].senha,user_a_ser_atualizado[0].imagem,user_a_ser_atualizado[0].descricao]
        elif user_a_ser_atualizado_arg == 'professor-tutor':
            campos_atigos_do_user = [user_a_ser_atualizado[0].nome,user_a_ser_atualizado[0].email,user_a_ser_atualizado[0].senha,user_a_ser_atualizado[0].imagem,user_a_ser_atualizado[0].descricao,user_a_ser_atualizado[0].eletiva]
        else:
            campos_atigos_do_user = [user_a_ser_atualizado[0].nome,user_a_ser_atualizado[0].email,user_a_ser_atualizado[0].senha,user_a_ser_atualizado[0].imagem,user_a_ser_atualizado[0].eletiva]
    elif user_a_ser_atualizado_arg == 'eletiva':
         #tente adicionar o user
        try:
            user_a_ser_atualizado.append(Eletivas.objects.get(id=id))
        #se não conseguir saía daqui
        except:
            menssagem_var['mensagem'] = "User não encontrado"
            return redirect(update_or_delete,u_or_d='atualizar', user_a_ser_atualizado_arg=user_a_ser_atualizado_arg)
        #já que chegou até aqui é porque está dando certo
        #entã, adicione à variável "model" o models do usuário e a pasta
        model.append(Eletivas.objects.all().values())
        model.append("img_eletivas")
        #adicionandos os campos antigos do usuário
        campos_atigos_do_user = [user_a_ser_atualizado[0].titulo,user_a_ser_atualizado[0].descricao,user_a_ser_atualizado[0].imagem,user_a_ser_atualizado[0].img_professores_eletiva,user_a_ser_atualizado[0].link]
    elif user_a_ser_atualizado_arg == 'admin':
         #tente pegar o user
        try:
            admin_a_ser_atualizado = Admins.objects.get(id=id)
        #se não conseguir saía daqui
        except:
            menssagem_var['mensagem'] = "User não encontrado"
            return redirect(update_or_delete,u_or_d='atualizar', user_a_ser_atualizado_arg=user_a_ser_atualizado_arg)
        #aqui é feita a verificação se o admin logado é o mesmo que será atualizado
        if admin_a_ser_atualizado.nome == request.session['nome_user_logado'] and 'atualizar' in request.session['lista_de_acoes'] :
            menssagem_var['mensagem'] = "Você não pode se auto atualizar"
            return redirect(update_or_delete,u_or_d='atualizar', user_a_ser_atualizado_arg=user_a_ser_atualizado_arg)
         #já que chegou até aqui é porque está dando certo
        #entã, adicione à variável "model" o models do usuário e a pasta
        model.append(Admins.objects.all().values())
        model.append("imagem_admins")
        #adicionando à variável "user_a_ser_atualizado" o user a ser atualizado
        user_a_ser_atualizado.append(admin_a_ser_atualizado)
        campos_atigos_do_user = [user_a_ser_atualizado[0].nome,user_a_ser_atualizado[0].email,user_a_ser_atualizado[0].senha,user_a_ser_atualizado[0].imagem,user_a_ser_atualizado[0].acoes]
 
    if request.method == 'POST':
        #pegando os novos valores, estes aqui são padrão(têm na maioria dos users)
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        imagem = request.FILES.get('imagem')
        #caso seja eletivas eu preciso saber se o usuário quer deixar sem imagens ou não
        pergunta_imagem = request.POST.get('pergunta_imagem')
        pergunta_imagem_professores = request.POST.get('pergunta_imagem_professores')
        #vaiável que recebe os novos campos do user
        campos_atualizados_do_user = []
        #ifs que pegão valores atuais dos usuarios
        if user_a_ser_atualizado_arg == 'professor': 
            #pegue a nova eletiva
            eletiva = request.POST.get('eletiva')
            #atualizando a variável "campos_atualizados_do_user"
            campos_atualizados_do_user = [nome,email,senha,imagem,eletiva]

        elif user_a_ser_atualizado_arg == 'tutor' or user_a_ser_atualizado_arg == 'professor-tutor':
            #pegue a nova descrição
            descricao = request.POST.get('descricao')
            if user_a_ser_atualizado_arg == 'professor-tutor':
                #pegue a nova eletiva
                eletiva = request.POST.get('eletiva')
                #campo caso seja professor-tutor
                campos_atualizados_do_user = [nome,email,senha,imagem,descricao,eletiva]
            else:
                #campo caso seja tutor
                campos_atualizados_do_user = [nome,email,senha,imagem,descricao]
        elif user_a_ser_atualizado_arg == 'eletiva':
            #a eletiva é o único "user" com campos diferentes, por isso a variável "campos_atualizados_do_user" é diferente das demais
            titulo = request.POST.get('titulo')
            link = request.POST.get('link')
            descricao = request.POST.get('descricao')
            img_professores = request.FILES.get('img_professores')
            campos_atualizados_do_user = [titulo,descricao,imagem,img_professores,link]
        elif user_a_ser_atualizado_arg == 'admin':
            #checkboxes do admin
            checkboxes = ['deletar','atualizar','cadastrar']
            acoes_permitidas = ""
            #loop que pega os respectivos valores dos checkboxes no html
            for i in checkboxes:
                checkbox = request.POST.get(i)
                if checkbox == 'on':
                    acoes_permitidas += f' {i}'
            #atualizando a variável "campos_atualizados_do_user"
            campos_atualizados_do_user = [nome,email,senha,imagem,acoes_permitidas]
        #esta variável é quem diz qual campo esta sendo atualizado no momento, por exemplo:
        #0: nome, 1: email ...
        tam = 0
        #for que percorre os novos valores inseridos pelo usuário 
        for i in campos_atualizados_do_user:
            #se o campo da vez for diferente do campo antigo, então...
            if i != campos_atigos_do_user[tam]:
                #se tam == 0 ou seja "nome"
                if tam == 0:
                    #se for eletiva
                    if user_a_ser_atualizado_arg == 'eletiva':
                        #muda também o nome no campo "eletiva" no models dos Professores
                        professores = Professores.objects.filter(eletiva=str(user_a_ser_atualizado[0].titulo))
                        # alunos = Alunos.objects.filter(eletiva=str(user_a_ser_atualizado[0].titulo))
                        #se o tamanho desta variável for diferente de 0 é porque há professores nesta eletiva e por isso devem ser alterados
                        if len(professores) != 0:
                            for p in professores:
                                p.eletiva = i
                                p.save()
                        #atualizando o título da eletiva
                        user_a_ser_atualizado[0].titulo = i
                    else:
                        #atualizando o nome do user
                        user_a_ser_atualizado[0].nome = i
                #tam == 1  and user != 'eletiva': email
                elif tam == 1 and user_a_ser_atualizado_arg != 'eletiva':
                    user_a_ser_atualizado[0].email = i
                #tam == 2  and user != 'eletiva': senha
                elif tam == 2 and user_a_ser_atualizado_arg != 'eletiva':
                    user_a_ser_atualizado[0].senha = i
                #tam == 2  and user == 'eletiva': foto de fundo da eletiva
                #tam == 3  and user != 'eletiva': foto de perfil do usuário
                elif tam == 3 and user_a_ser_atualizado_arg != 'eletiva' or tam == 2 and user_a_ser_atualizado_arg == 'eletiva' :
                    #se não for passada imagem nova ou se for e o input que diz se o usuário quer ou não deixar sem imagem
                    #estiver marcado então chamará a função "checar_imagem_existente" como None
                    if imagem != None and pergunta_imagem == 'on' or imagem == None and pergunta_imagem == 'on':
                        user_a_ser_atualizado[0].imagem = checar_imagem_existente(None,model[1],'atualizar')
                    #do contrário chamará a função "checar_imagem_existente" com a nova imagem 
                    elif imagem != None and pergunta_imagem == None:
                        user_a_ser_atualizado[0].imagem = checar_imagem_existente(imagem,model[1],'atualizar')
                #tam == 3  and user == 'eletiva': foto dos professores
                elif tam == 3 and user_a_ser_atualizado_arg == 'eletiva':
                    #se for inserida uma imagem ou não e o input que diz que o usuário quer deixar sem imagem estiver marcado então chamará a função "checar_imagem_existente" como None
                    if img_professores != None and pergunta_imagem_professores == 'on' or img_professores == None and pergunta_imagem_professores == 'on':
                        user_a_ser_atualizado[0].img_professores_eletiva = checar_imagem_existente(None,f'img_eletivas/img_professores_eletiva','atualizar')
                    #caso contrário chamará "checar_imagem_existente" com a nova imagem 
                    elif img_professores != None and pergunta_imagem_professores == None:
                        user_a_ser_atualizado[0].img_professores_eletiva = checar_imagem_existente(img_professores,f'img_eletivas/img_professores_eletiva','atualizar')
                #na posição 4 da variável "campos_atualizados_do_user" do admin, tutor e professor-tutor esta localizado o campo diferente de "eletiva"
                elif tam == 4 and user_a_ser_atualizado_arg != 'admin' and user_a_ser_atualizado_arg != 'tutor' and user_a_ser_atualizado_arg != 'professor-tutor' or tam == 5 and user_a_ser_atualizado_arg == 'professor-tutor':
                    user_a_ser_atualizado[0].eletiva = i
                #a posição 4 da variável "campos_atualizados_do_user" do admin é equivalente ao campo "acoes"
                elif tam == 4 and user_a_ser_atualizado_arg == 'admin':
                    user_a_ser_atualizado[0].acoes = i
                #a posição 4 da variável "campos_atualizados_do_user" do tutor e professor-tutor é equivalente ao campo "descricao"
                #a posição 1 da variável "campos_atualizados_do_user" da eletiva também é equivalente ao campo "descricao"
                elif tam == 4 and user_a_ser_atualizado_arg == 'tutor' or  tam == 4 and user_a_ser_atualizado_arg == 'professor-tutor' or user_a_ser_atualizado_arg == 'eletiva' and tam == 1:
                    user_a_ser_atualizado[0].descricao = i
            #aumentando o valor da variável "tam" para que seja mantido o fluxo
            tam += 1
        #salvando as alterações efetuadas
        user_a_ser_atualizado[0].save()
        #como a eletiva possui 2 cmpos com imagens, eu presciso chamar o campo "img_professores_eletiva"
        if user_a_ser_atualizado_arg == 'eletiva':
            excluir_imagem(f'{model[1]}/img_professores_eletiva',model[0])
        #excluindo as imagens que não estão sendo mais utilizadas. model[1]: Todos os valores do models no qual está indserido o user que foi atualizado, model[0]: Pasta no qual esta situada as imagens do models
        excluir_imagem(model[1],model[0])
        #adicionado uma nova mensagem
        menssagem_var['mensagem'] = "Atualizado com sucesso!"
        return redirect(update_or_delete,u_or_d='atualizar',user_a_ser_atualizado_arg=user_a_ser_atualizado_arg)
    else:
        #tipo do user a ser atualizado, o user passado como parâmetro
        dados['user_a_ser_atualizado_arg'] = user_a_ser_atualizado_arg
        #recebe o user que será atualizado
        dados['tabela'] = user_a_ser_atualizado[0]
        dados['eletivas'] = Eletivas.objects
        dados['eletivas_para_for'] = Eletivas.objects.all().values()
        #só se o tipo de user for um "professor" ou um "professor-tutor" será necessário verificar as eletivas
        if user_a_ser_atualizado_arg == 'professor' or user_a_ser_atualizado_arg == 'professor-tutor':
            #percorre os valores das eletivas
            for i in dados['eletivas_para_for']:
                #pega os professores que estão cadastrados na eletiva da vez
                p = Professores.objects.filter(eletiva=i['titulo'])
                #se for igual a 2 é porque a eletiva esta completa
                if len(p) == 2:
                    dados['eletivas'] = dados['eletivas'].exclude(titulo=i['titulo'])
        #atualizando a variável "dados['eletivas']" para receber os valores dos objects e não os objects
        dados['eletivas'] = dados['eletivas'].values()
        #tamanho equivalente ao total de eletivas não completas
        dados['tamanho_eletivas'] = len(dados['eletivas'])
        dados['message'] = ''
        #caso o "user_a_ser_atualizado_arg" seja um admin é necessário que maque os inputs que equivalem as ações que ele pode efetuar
        if user_a_ser_atualizado_arg == 'admin':
            #passando as ações do admin para list
            acoes_lista = campos_atigos_do_user[4].split()
            #percorrendo a lista acima
            for i in acoes_lista:
                #checked, no html equivale a "marcado"
                dados[f'{i}'] = 'checked'
        return render(request, 'atualizar/atualizar_com_id.html', dados)
    
def definir_paginas_utilizaveis(request):
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'definirpaginas') == True:
        return redirect(retornar_index)
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

def add_OqueTemosaOferecer(request):
    if dados_universsais['user'] != 'ADMIN':
        menssagem_var['mensagem'] = 'Somente o ADMIN(diretor) pode adicionar os oferecimentos'
        return redirect(retornar_index)
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        imagem = checar_imagem_existente(request.FILES.get('imagem'),'img_OqueTemosaOferecer','cadastrar')
        descricao = request.POST.get('descricao')
        link = request.POST.get('link')
        titulo_link = request.POST.get('titulo_link')

        novo_oferecimento = OqueTemosaOferecer(titulo=titulo,imagem=imagem,descricao=descricao,link=link,titulo_do_link=titulo_link)
        novo_oferecimento.save()
        menssagem_var['mensagem'] = "Oferecimento adicionado"
        return redirect(retornar_index)
    else:
        return render(request,'OqueTemosaOferecer/add_oferecimentos.html')

def editar_oferecimento(request,id):
    if dados_universsais['user'] != 'ADMIN':
        menssagem_var['mensagem'] = 'Somente o ADMIN(diretor) pode editar os oferecimentos'
        return redirect(retornar_index)
    dados = {}
    try:
        oferecimento_a_ser_atualizado = OqueTemosaOferecer.objects.get(id=id)
    except:
        menssagem_var['mensagem'] = "Id não encontrado"
        return redirect(retornar_index)
    dados['titulo'] = oferecimento_a_ser_atualizado.titulo
    dados['descricao'] = oferecimento_a_ser_atualizado.descricao
    dados['imagem'] = oferecimento_a_ser_atualizado.imagem
    dados['link'] = oferecimento_a_ser_atualizado.link
    dados['titulo_do_link'] = oferecimento_a_ser_atualizado.titulo_do_link
    if request.method == 'POST':
        titulo_novo= request.POST.get('titulo')
        descricao_nova = request.POST.get('descricao')
        imagem_nova = request.FILES.get('imagem')
        link_novo = request.POST.get('link')
        titulo_link_novo = request.POST.get('titulo_link')
        
        
        if dados['titulo'] != titulo_novo:
            oferecimento_a_ser_atualizado.titulo = titulo_novo
        if dados['descricao'] != descricao_nova:
            oferecimento_a_ser_atualizado.descricao = descricao_nova
        if dados['link'] != link_novo:
            oferecimento_a_ser_atualizado.link = link_novo
        if dados['titulo_do_link'] != titulo_link_novo:
            oferecimento_a_ser_atualizado.titulo_do_link = titulo_link_novo
        if imagem_nova != None:
            oferecimento_a_ser_atualizado.imagem = checar_imagem_existente(imagem_nova,'img_OqueTemosaOferecer','atualizar')
            excluir_imagem('img_OqueTemosaOferecer',OqueTemosaOferecer.objects.all().values())
      
        oferecimento_a_ser_atualizado.save()
        menssagem_var['mensagem'] = "Oferecimento atualizado"
        return redirect(retornar_index)
    else:
        return render(request, 'OqueTemosaOferecer/editar_oferecimento.html', dados)

def add_professor_carrossel(request):
    if request.method == 'POST':
        ids = request.POST.get('ids')
        campo = CarrosselProfessores.objects.get(id=1)
        campo.ids = ids
        campo.save()
        return redirect(eletivas)
    else:
        dados = dados_universsais.copy()
        dados['usuarios'] = Professores.objects.filter(tutor=True).values()
        dados['modo'] = 'adicionarcarrossel'
        return render(request,'definir_carrossel/tabela_com_os_tutores.html',dados)




