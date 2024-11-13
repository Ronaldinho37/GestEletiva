from ...views import menssagem_var
from ...models import Professores,Admins,Eletivas
from django.shortcuts import render, redirect
from ..funcoes_sem_url.excluir_imagem import excluir_imagem
from ..funcoes_sem_url.checar_imagem import checar_imagem_existente
from ..funcoes_sem_url.acao_requisitada import verificar_se_o_usuario_pode_realizar_a_acao_equisitada

#mudar o tamanho da lista
#função que atualiza 
def update_com_id(request,user_a_ser_atualizado_arg,id):
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'atualizar') == True:
        return redirect("/")
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
            return redirect(f"/area-restrita/update_or_delete/atualizar/{user_a_ser_atualizado_arg}")
        if user_a_ser_atualizado[0].tutor == True and user_a_ser_atualizado[0].professor == True and user_a_ser_atualizado_arg != 'professor-tutor':
            return redirect(update_com_id, user_a_ser_atualizado_arg='professor-tutor',id=id)
        #já que chegou até aqui é porque está dando certo
        #entã, adicione à variável "model" o models do usuário e a pasta
        model.append(Professores.objects.all().values())
        model.append("imagem_professores")
        # #como tutores, professores e professores-tutores têm campos diferentes, estes ifs adicionam somente os campos necessários 
        # if user_a_ser_atualizado_arg == 'tutor':
        #     campos_atigos_do_user = {'nome': user_a_ser_atualizado[0].nome,'email': user_a_ser_atualizado[0].email,'idade':user_a_ser_atualizado[0].idade,'imagem':user_a_ser_atualizado[0].imagem,'descricao':user_a_ser_atualizado[0].descricao}
        # else:
        #     campos_atigos_do_user = {'nome': user_a_ser_atualizado[0].nome,'email': user_a_ser_atualizado[0].email,'idade':user_a_ser_atualizado[0].idade,'imagem':user_a_ser_atualizado[0].imagem,'descricao':user_a_ser_atualizado[0].descricao,'eletiva':user_a_ser_atualizado[0].eletiva,'graduacao':user_a_ser_atualizado[0].graduacao}
    elif user_a_ser_atualizado_arg == 'eletiva':
         #tente adicionar o user
        try:
            user_a_ser_atualizado.append(Eletivas.objects.get(id=id))
        #se não conseguir saía daqui
        except:
            menssagem_var['mensagem'] = "User não encontrado"
            return redirect(f"/area-restrita/update_or_delete/atualizar/{user_a_ser_atualizado_arg}")
        #já que chegou até aqui é porque está dando certo
        #entã, adicione à variável "model" o models do usuário e a pasta
        model.append(Eletivas.objects.all().values())
        model.append("img_eletivas")
        #adicionandos os campos antigos do usuário
        campos_atigos_do_user = {'titulo':user_a_ser_atualizado[0].titulo,'descricao':user_a_ser_atualizado[0].descricao,'imagem':user_a_ser_atualizado[0].imagem,'img_professores':user_a_ser_atualizado[0].img_professores_eletiva,'link':user_a_ser_atualizado[0].link}
    elif user_a_ser_atualizado_arg == 'admin':
         #tente pegar o user
        try:
            admin_a_ser_atualizado = Admins.objects.get(id=id)
        #se não conseguir saía daqui
        except:
            menssagem_var['mensagem'] = "User não encontrado"
            return redirect(f"/area-restrita/update_or_delete/atualizar/{user_a_ser_atualizado_arg}")
        #aqui é feita a verificação se o admin logado é o mesmo que será atualizado
        if admin_a_ser_atualizado.nome == request.session['nome_user_logado'] and 'atualizar' in request.session['lista_de_acoes'] :
            menssagem_var['mensagem'] = "Você não pode se auto atualizar"
            return redirect(f"/area-restrita/update_or_delete/atualizar/{user_a_ser_atualizado_arg}")
         #já que chegou até aqui é porque está dando certo
        #entã, adicione à variável "model" o models do usuário e a pasta
        model.append(Admins.objects.all().values())
        model.append("imagem_admins")
        #adicionando à variável "user_a_ser_atualizado" o user a ser atualizado
        user_a_ser_atualizado.append(admin_a_ser_atualizado)
        campos_atigos_do_user = {'nome':user_a_ser_atualizado[0].nome,'email':user_a_ser_atualizado[0].email,'senha':user_a_ser_atualizado[0].senha,'imagem':user_a_ser_atualizado[0].imagem,'acoes':user_a_ser_atualizado[0].acoes}
 
    if request.method == 'POST':
        dados_request = {}
        def definir_requests(request,campos_antigos_do_user_arg):
            for i in campos_antigos_do_user_arg:
                if i == 'imagem' or i == 'img_professores':
                    dados_request[f'{i}'] = request.FILES.get(f'{i}')
                else:
                    dados_request[f'{i}'] = request.POST.get(f'{i}')
        dados_request['pergunta_imagem'] = request.POST.get('pergunta_imagem')
        #vaiável que recebe os novos campos do user
        campos_atualizados_do_user = []
        #ifs que pegão valores atuais dos usuarios
        if user_a_ser_atualizado_arg == 'professor' or user_a_ser_atualizado_arg == 'professor-tutor' or user_a_ser_atualizado_arg == 'tutor': 
            professor = request.POST.get('professor')
            tutor = request.POST.get('tutor')
            if professor == 'on' and tutor != 'on' and user_a_ser_atualizado_arg != 'professor':
                user_a_ser_atualizado[0].professor = True
                user_a_ser_atualizado[0].tutor = False
                user_a_ser_atualizado_arg = "professor"
            elif professor != 'on' and tutor == 'on' and user_a_ser_atualizado_arg != 'tutor':
                user_a_ser_atualizado[0].tutor = True
                user_a_ser_atualizado[0].professor = False
                user_a_ser_atualizado_arg = "tutor"
            elif professor != 'on' and tutor != 'on' and user_a_ser_atualizado_arg != 'professor-tutor':
                user_a_ser_atualizado[0].professor = True
                user_a_ser_atualizado[0].tutor = True
                user_a_ser_atualizado_arg = "professor-tutor"
                
            campos_atigos_do_user.clear()
            campos_atigos_do_user = {'nome': user_a_ser_atualizado[0].nome,'email': user_a_ser_atualizado[0].email,'idade':user_a_ser_atualizado[0].idade,'imagem':user_a_ser_atualizado[0].imagem,'descricao':user_a_ser_atualizado[0].descricao,'eletiva':user_a_ser_atualizado[0].eletiva,'graduacao':user_a_ser_atualizado[0].graduacao}
            definir_requests(request,campos_atigos_do_user)
            if user_a_ser_atualizado[0].tutor == True and user_a_ser_atualizado[0].professor == False:
                campos_atualizados_do_user = [dados_request['nome'],dados_request['email'],dados_request['idade'],dados_request['imagem'],dados_request['descricao'],"",""]
            else:
                campos_atualizados_do_user = [dados_request['nome'],dados_request['email'],dados_request['idade'],dados_request['imagem'],dados_request['descricao'],dados_request['eletiva'],dados_request['graduacao']]

        elif user_a_ser_atualizado_arg == 'eletiva':
                    #caso seja eletivas eu preciso saber se o usuário quer deixar sem imagens ou não
            dados_request['pergunta_imagem_professores'] = request.POST.get('pergunta_imagem_professores')
            campos_atualizados_do_user = [dados_request['titulo'],dados_request['descricao'],dados_request['imagem'],dados_request['img_professores'],dados_request['link']]
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
            campos_atualizados_do_user = [dados_request['nome'],dados_request['email'],dados_request['senha'],dados_request['imagem'],acoes_permitidas]
        
        #esta variável é quem diz qual campo esta sendo atualizado no momento, por exemplo:
        #0: nome, 1: email ...
        tam = 0
        print(user_a_ser_atualizado_arg)
        print(user_a_ser_atualizado[0].professor)
        print(user_a_ser_atualizado[0].tutor)
        for i in campos_atualizados_do_user:
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
            #pois na posicao 1 de eletivas está 'descrição'
            elif tam == 1 and user_a_ser_atualizado_arg != 'eletiva':
                user_a_ser_atualizado[0].email = i      
            elif tam == 2 and user_a_ser_atualizado_arg != 'admin' and user_a_ser_atualizado_arg != 'eletiva':
                user_a_ser_atualizado[0].idade = i 
            elif tam == 2 and user_a_ser_atualizado_arg == 'admin':
                user_a_ser_atualizado[0].senha = i
            elif tam == 3 and user_a_ser_atualizado_arg == 'eletiva':
                if dados_request['pergunta_imagem_professores'] != 'on':
                    if i != None:
                        user_a_ser_atualizado[0].img_professores_eletiva = checar_imagem_existente(i,'eletivas/img_professores_eletiva',None)
                else:
                    user_a_ser_atualizado[0].img_professores_eletiva = checar_imagem_existente(None,'eletivas/img_professores_eletiva',None)
            elif tam == 3 and user_a_ser_atualizado_arg != 'eletiva' or tam == 2 and user_a_ser_atualizado_arg == 'eletiva':
                if dados_request['pergunta_imagem'] != 'on':
                    if i != None:
                        user_a_ser_atualizado[0].imagem = checar_imagem_existente(i,model[1],None)
                else:
                    user_a_ser_atualizado[0].imagem = checar_imagem_existente(None,model[1],None)
            elif tam == 4 and user_a_ser_atualizado_arg == 'admin':
                user_a_ser_atualizado[0].acoes = i
            elif tam == 4 and user_a_ser_atualizado_arg == 'eletiva':
                user_a_ser_atualizado[0].link = i
            elif tam == 4 and user_a_ser_atualizado_arg != 'eletiva' and user_a_ser_atualizado_arg != 'admin' or tam == 1 and user_a_ser_atualizado_arg == 'eletiva':
                user_a_ser_atualizado[0].descricao = i  
            elif tam == 5 and user_a_ser_atualizado_arg == 'tutor':
                user_a_ser_atualizado[0].eletiva = ""
            elif tam == 5 and user_a_ser_atualizado_arg == 'professor' or tam == 5 and user_a_ser_atualizado_arg == 'professor-tutor':
                user_a_ser_atualizado[0].eletiva = i 
            elif tam == 6 and user_a_ser_atualizado_arg == 'tutor':
                user_a_ser_atualizado[0].graduacao = ""
            elif tam == 6 and user_a_ser_atualizado_arg == 'professor' or tam == 6 and user_a_ser_atualizado_arg == 'professor-tutor':
                user_a_ser_atualizado[0].graduacao = i
            
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
        return redirect(f"/area-restrita/update_or_delete/atualizar/{user_a_ser_atualizado_arg}")
    else:
        #tipo do user a ser atualizado, o user passado como parâmetro
        dados['user_a_ser_atualizado_arg'] = user_a_ser_atualizado_arg
        #recebe o user que será atualizado
        dados['tabela'] = user_a_ser_atualizado[0]
        dados['eletivas'] = Eletivas.objects
        dados['eletivas_para_for'] = Eletivas.objects.all().values()            
        #atualizando a variável "dados['eletivas']" para receber os valores dos objects e não os objects
        dados['eletivas'] = dados['eletivas'].values()
        #tamanho equivalente ao total de eletivas não completas
        dados['tamanho_eletivas'] = len(dados['eletivas'])
        dados['message'] = ''
        #caso o "user_a_ser_atualizado_arg" seja um admin é necessário que maque os inputs que equivalem as ações que ele pode efetuar
        if user_a_ser_atualizado_arg == 'admin':
            #passando as ações do admin para list
            acoes_lista = campos_atigos_do_user['acoes'].split()
            #percorrendo a lista acima
            for i in acoes_lista:
                #checked, no html equivale a "marcado"
                dados[f'{i}'] = 'checked'
        elif user_a_ser_atualizado_arg == 'tutor' or user_a_ser_atualizado_arg == 'professor' or user_a_ser_atualizado_arg == 'professor-tutor':
            #percorre os valores das eletivas
            for i in dados['eletivas_para_for']:
                #pega os professores que estão cadastrados na eletiva da vez
                p = Professores.objects.filter(eletiva=i['titulo'])
                #se for igual a 2 é porque a eletiva esta completa
                if len(p) == 2:
                    dados['eletivas'] = dados['eletivas'].exclude(titulo=i['titulo'])
            if dados['tabela'].tutor == False and dados['tabela'].professor == True:
                dados["tutor"] = ""
                dados["professor"] = "checked"
                dados["professor_tutor"] = ""
            elif dados['tabela'].tutor == True and dados['tabela'].professor == False:
                dados["tutor"] = "checked"
                dados["professor"] = ""
                dados["professor_tutor"] = ""
            else:
                dados["tutor"] = ""
                dados["professor"] = ""
                dados["professor_tutor"] = "checked"
        return render(request, 'atualizar/atualizar_com_id.html', dados)