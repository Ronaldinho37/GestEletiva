from django.shortcuts import render, redirect
from ...models import Admins
from ..funcoes_sem_url.para_onde_vou import para_onde_vou
from ..funcoes_sem_url.acao_requisitada import verificar_se_o_usuario_pode_realizar_a_acao_equisitada
from ..funcoes_sem_url.checar_imagem import checar_imagem_existente
from ...views import dados_universsais,menssagem_var
#função que adiciona o admin
def add_admin(request):
    if dados_universsais['user'] == 'admin':
        if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
            return redirect("/")
    
    if request.method == 'POST':
        nome = request.POST.get('nome').lower()
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        link_antigoA = request.POST.get('link_antigoA')
        imagem = checar_imagem_existente(request.FILES.get('imagem'),'imagem_admins', None)
        print(link_antigoA)
        

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
        menssagem_var['mensagem'] = "Admin adicionado com sucesso!"
        return para_onde_vou(request,link_antigo=link_antigoA)
    else:
        return render(request,'acoes_principais/template_add.html')