from ...views import dados_universsais,menssagem_var
from ...models import Professores,Admins,Eletivas,OqueTemosaOferecer
from ..funcoes_sem_url.excluir_imagem import excluir_imagem
from ..funcoes_sem_url.acao_requisitada import verificar_se_o_usuario_pode_realizar_a_acao_equisitada
from django.shortcuts import render, redirect
def deletar_com_ids(request,user_a_ser_atualizado_arg,id):
        #verificando se o usuário pode deletar
        if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'deletar') == True:
            return redirect("/")
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
                    return redirect(f"/area-restrita/update_or_delete/deletar/{user_a_ser_atualizado_arg}")
        
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
                            return redirect(f"/area-restrita/update_or_delete/deletar/{user_a_ser_atualizado_arg}")
                #se o user_a_ser_atualizado_arg for um professor ou tutor
                elif user_a_ser_atualizado_arg == 'oferecimento':
                    if dados['user'] != 'ADMIN':
                        menssagem_var['mensagem'] = 'somente o ADMIN(diretor) pode deletar o oferecimentos'
                        return redirect("/")
                    else:
                        id_a_ser_deletado = dados['lista_id'][0]
                        dados['model_user'] = OqueTemosaOferecer.objects.all().values()
                        dados['diretorio_user'] = "img_OqueTemosaOferecer"
                        try:
                            OqueTemosaOferecer.objects.get(id=id_a_ser_deletado).delete()
                            excluir_imagem('img_OqueTemosaOferecer',OqueTemosaOferecer.objects.all().values())
                            menssagem_var['mensagem'] = 'O oferecimento foi deletado'
                        except:
                            menssagem_var['mensagem'] = 'Id não encontrado'
                        return redirect("/")
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
                                return redirect(f"/area-restrita/update_or_delete/deletar/{user_a_ser_atualizado_arg}")
                            else:
                                 #tente pegar o object de id = i e delete-o
                                try:
                                    Professores.objects.get(id=i).delete()
                                except:
                                     #se não conseguir saía daqui
                                    return redirect(f"/area-restrita/update_or_delete/deletar/{user_a_ser_atualizado_arg}")
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
                                return redirect(f"/area-restrita/update_or_delete/deletar/{user_a_ser_atualizado_arg}")
                            else:
                                try:
                                    Professores.objects.get(id=i).delete()
                                except:
                                    return redirect(f"/area-restrita/update_or_delete/deletar/{user_a_ser_atualizado_arg}")
                #se o user passado como parâmetro for igual a eletiva
                elif user_a_ser_atualizado_arg == "eletiva":
                    dados['model_user'] = Eletivas.objects.all().values()
                    dados['diretorio_user'] = "img_eletivas"
                    dados['user'] = 'eletiva(s)'
                    for i in dados['lista_id']:
                        try:
                            eletiva_a_ser_deletada = Eletivas.objects.get(id=i) #.delete()
                        except:
                            return redirect(f"/area-restrita/update_or_delete/deletar/{user_a_ser_atualizado_arg}")
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
                return redirect(f"/area-restrita/update_or_delete/deletar/{user_a_ser_atualizado_arg}")
            
            excluir_imagem(dados['diretorio_user'],dados['model_user'])
            #como a eletiva tem dois campos que requerem imagens, é necessário que a função 'excluir_imagem' seja chamada novamente, 
            #agora excluindo as imagens dos professores
            if dados['diretorio_user'] == 'img_eletivas':
               excluir_imagem(f"{dados['diretorio_user']}/img_professores_eletiva", dados['model_user'])
            menssagem_var['mensagem'] = f'Todo(s) o(s) {dados["tam_lista_id"]} {dados["user"]} deletado(s)'
            return redirect(f"/area-restrita/update_or_delete/deletar/{user_a_ser_atualizado_arg}")
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
                        return redirect(f"/area-restrita/update_or_delete/deletar/{user_a_ser_atualizado_arg}")
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