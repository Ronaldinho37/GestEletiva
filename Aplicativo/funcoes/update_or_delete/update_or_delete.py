from ...views import dados_universsais,menssagem_var
from ...models import Professores,Admins,Eletivas,CarrosselProfessores
from ..funcoes_sem_url.acao_requisitada import verificar_se_o_usuario_pode_realizar_a_acao_equisitada

from django.shortcuts import render, redirect
#função que direciona o usuário para a página de Deletar ou Atualizar, com respectivas variáveis necessárias
def update_or_delete(request,u_or_d,user_a_ser_atualizado_arg):
    #caso a variável passada na url seja diferente das ações que esta função pode realizar
    if u_or_d != 'deletar' and u_or_d != 'atualizar':
        return redirect("/")

    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,f'{u_or_d}') == True:
        return redirect("/")
   
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
    elif user_a_ser_atualizado_arg.lower() == 'carrossel':
        dados['usuarios'] = CarrosselProfessores.objects.all().values()
    #caso seja nenhum dos acima
    else:
        menssagem_var['mensagem'] = "Usuário não identificado"
        return redirect("/")
    #pegando a menssagem
    dados['message'] = menssagem_var['mensagem'] 
    #apagando-a da variável "menssagem_var", isso significa que ela já foi usada
    menssagem_var['mensagem'] = ""
    #retornando para a respectiva página
    return render(request,f'{u_or_d}/{u_or_d}.html', dados)