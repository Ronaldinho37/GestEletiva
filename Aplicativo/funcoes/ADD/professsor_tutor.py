
from django.shortcuts import render, redirect
from ...models import Professores,Eletivas
from ..funcoes_sem_url.checar_imagem import checar_imagem_existente
from ..funcoes_sem_url.acao_requisitada import verificar_se_o_usuario_pode_realizar_a_acao_equisitada
from ...views import menssagem_var
#função que adiciona os professores e/ou tutores
#tipo_de_user: tipo do user a ser adicionado(professor/tutor)
def add_professor(request, tipo_de_user):
    #chama a função que verifica se o usuário está apto ou não à adicionar professores ou não
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
        return redirect("/")

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
            return redirect("/tutoria")
        elif tipo_de_user == 'professor-tutor':
            menssagem_var['mensagem'] = "Professor/tutor adicionado!"
            return redirect("/eletivas")
        else:
            menssagem_var['mensagem'] = "Professor adicionado!"
            return redirect("/eletivas")
    else:
        dados={}
        try:
            dados['message'] = menssagem_var['mensagem']
            menssagem_var['mensagem'] = ""
        except:
            dados['message'] = ''
        #como essa função só adiciona professor ou tutor, se o 'tipo_de_user' for difente não poderá ser adicionado
        if tipo_de_user != 'professor' and tipo_de_user != 'tutor' and tipo_de_user != 'professor-tutor':
            return redirect("/")
        #como há campos pertencentes ao professor que são diferentes dos campos de um tutor
        #nesta variável eu retorno o tipo do user, e lá no html,através de um if só será mostrado os campos referentes ao user a ser adicionado
        dados['tipo_de_user'] = tipo_de_user
        #recebe as eletivas: poderei executar o 'exclude'
        dados['eletivas'] = Eletivas.objects
         #recebe as eletivas: não poderei executar o 'exclude', porém, percorrerei-a para verificar se há eletivas sem professores
        dados['eletivas_para_for'] = Eletivas.objects.all().values()
        if len(dados['eletivas_para_for']) == 0:
            return redirect("/")
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
                        return redirect("/eletivas")
                # elif len(p) == 0:
                #     dados['eletivas'] = dados['eletivas'].all().values()
        #como eu tinha que executar o 'exclude' eu não podia obter os 'values' do models 'Eletivas', porém, agora posso
        dados['eletivas'] = dados['eletivas'].values()
        return render(request,'professor/addprofessor.html',dados)