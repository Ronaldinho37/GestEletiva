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
        #como tutores, professores e professores-tutores têm campos diferentes, estes ifs adicionam somente os campos necessários 
        if user_a_ser_atualizado_arg == 'tutor':
            campos_atigos_do_user = [user_a_ser_atualizado[0].nome,user_a_ser_atualizado[0].email,user_a_ser_atualizado[0].idade,user_a_ser_atualizado[0].imagem,user_a_ser_atualizado[0].descricao]
        else:
            campos_atigos_do_user = [user_a_ser_atualizado[0].nome,user_a_ser_atualizado[0].email,user_a_ser_atualizado[0].idade,user_a_ser_atualizado[0].imagem,user_a_ser_atualizado[0].descricao,user_a_ser_atualizado[0].eletiva,user_a_ser_atualizado[0].graduacao]
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
        campos_atigos_do_user = [user_a_ser_atualizado[0].titulo,user_a_ser_atualizado[0].descricao,user_a_ser_atualizado[0].imagem,user_a_ser_atualizado[0].img_professores_eletiva,user_a_ser_atualizado[0].link]
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
        campos_atigos_do_user = [user_a_ser_atualizado[0].nome,user_a_ser_atualizado[0].email,user_a_ser_atualizado[0].senha,user_a_ser_atualizado[0].imagem,user_a_ser_atualizado[0].acoes]
 
    if request.method == 'POST':
        #pegando os novos valores, estes aqui são padrão(têm na maioria dos users)
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        imagem = request.FILES.get('imagem')
        idade = request.POST.get('idade')
        graduacao = request.POST.get('graduacao')
        #pegue a nova eletiva
        eletiva = request.POST.get('eletiva')
        #pegue a nova descrição
        descricao = request.POST.get('descricao')
        #caso seja eletivas eu preciso saber se o usuário quer deixar sem imagens ou não
        pergunta_imagem = request.POST.get('pergunta_imagem')
        pergunta_imagem_professores = request.POST.get('pergunta_imagem_professores')
        #vaiável que recebe os novos campos do user
        campos_atualizados_do_user = []
        #ifs que pegão valores atuais dos usuarios
        if user_a_ser_atualizado_arg == 'professor' or user_a_ser_atualizado_arg == 'professor-tutor' or user_a_ser_atualizado_arg == 'tutor': 
            professor = request.POST.get('professor')
            tutor = request.POST.get('tutor')
            if professor == 'on' and tutor != 'on':
                user_a_ser_atualizado[0].professor = True
                user_a_ser_atualizado[0].tutor = False
                user_a_ser_atualizado_arg = "professor"
            elif professor != 'on' and tutor == 'on':
                user_a_ser_atualizado[0].tutor = True
                user_a_ser_atualizado[0].professor = False
                user_a_ser_atualizado_arg = "tutor"
                #ta dando erro porque o user_a_ser_atualizado_arg precisa mudar
            else:
                user_a_ser_atualizado[0].professor = True
                user_a_ser_atualizado[0].tutor = True
                user_a_ser_atualizado_arg = "professor-tutor"
                
            if user_a_ser_atualizado_arg == 'tutor':
                #campo caso seja tutor
                campos_atualizados_do_user = [nome,email,idade,imagem,descricao]
            else:
                #atualizando a variável "campos_atualizados_do_user"
                if user_a_ser_atualizado[0].tutor == True and user_a_ser_atualizado[0].professor == False:
                    eletiva = ""
                campos_atualizados_do_user = [nome,email,idade,imagem,eletiva,descricao,graduacao]
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
                elif tam == 2 and user_a_ser_atualizado_arg != 'eletiva' and user_a_ser_atualizado_arg != 'professor' and user_a_ser_atualizado_arg != 'tutor' and user_a_ser_atualizado_arg != 'professor-tutor':
                    user_a_ser_atualizado[0].senha = i
                elif tam == 2 and user_a_ser_atualizado_arg != 'professor' or tam == 2 and user_a_ser_atualizado_arg != 'professor-tutor' or tam == 2 and user_a_ser_atualizado_arg != 'tutor':
                    user_a_ser_atualizado[0].idade = i
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
                elif tam == 4 and user_a_ser_atualizado_arg != 'admin' and user_a_ser_atualizado_arg != 'tutor' and user_a_ser_atualizado_arg == 'professor-tutor':
                    user_a_ser_atualizado[0].eletiva = i
                #a posição 4 da variável "campos_atualizados_do_user" do admin é equivalente ao campo "acoes"
                elif tam == 4 and user_a_ser_atualizado_arg == 'admin':
                    user_a_ser_atualizado[0].acoes = i
                #a posição 4 da variável "campos_atualizados_do_user" do tutor e professor-tutor é equivalente ao campo "descricao"
                #a posição 1 da variável "campos_atualizados_do_user" da eletiva também é equivalente ao campo "descricao"
                elif tam == 4 and user_a_ser_atualizado_arg == 'tutor' or  tam == 5 and user_a_ser_atualizado_arg == 'professor-tutor' or user_a_ser_atualizado_arg == 'eletiva' and tam == 1 or user_a_ser_atualizado_arg == 'professor' and tam == 5 :
                    user_a_ser_atualizado[0].descricao = i
                elif tam == 6 and user_a_ser_atualizado_arg == 'professor' or tam == 6 and user_a_ser_atualizado_arg == 'professor-tutor':
                    user_a_ser_atualizado[0].graduacao = i
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
        return redirect(f"/area-restrita/update_or_delete/atualizar/{user_a_ser_atualizado_arg}")
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
        elif user_a_ser_atualizado_arg == 'tutor' or user_a_ser_atualizado_arg == 'professor' or user_a_ser_atualizado_arg == 'professor-tutor':
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