from ...views import menssagem_var
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