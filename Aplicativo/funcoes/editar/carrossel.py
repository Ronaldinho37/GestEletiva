from ...views import dados_universsais,menssagem_var
from ...models import CarrosselProfessores
from ..funcoes_sem_url.checar_imagem import checar_imagem_existente
from ..funcoes_sem_url.excluir_imagem import excluir_imagem
from django.shortcuts import render, redirect

def update_carrossel(request,id):
    dados = dados_universsais.copy()
    if dados['user'] != 'ADMIN':
        menssagem_var['mensagem'] = "Só o diretor pode editar o carrossel"
        return redirect("/eletivas")
    usuario = CarrosselProfessores.objects.get(id=int(id))
    dados['nome'] = usuario.nome
    dados['idade'] = usuario.idade
    dados['graduacao'] = usuario.graduacao
    dados['imagem'] = usuario.imagem
    dados['descricao'] = usuario.descricao
    if request.method == 'POST':
        novo_nome = request.POST.get('nome')
        nova_idade = request.POST.get('idade')
        nova_graduacao = request.POST.get('graduacao')
        nova_descricao = request.POST.get('descricao')
        novo_imagem = request.FILES.get('imagem')
        deixar_sem_imagem = request.POST.get('deixar_sem_imagem')
        if novo_nome != dados['nome']:
            usuario.nome = novo_nome
        if nova_graduacao != dados['graduacao']:
            usuario.graduacao = nova_graduacao
        if nova_idade != dados['idade']:
            usuario.idade = nova_idade
        if nova_descricao != dados['descricao']:
            usuario.descricao = nova_descricao
        if deixar_sem_imagem == 'on' and novo_imagem != None or deixar_sem_imagem == 'on' and novo_imagem == None:
            usuario.imagem = checar_imagem_existente(None,'carrosselProfessor',None)
        elif deixar_sem_imagem != 'on' and novo_imagem != None:
            usuario.imagem = checar_imagem_existente(novo_imagem,'carrosselProfessor',None)
            
        usuario.save()
        excluir_imagem('carrosselProfessores',CarrosselProfessores.objects.all().values())

        menssagem_var['mensagem'] = "Carrossel atualizado com sucesso"
        return redirect("/eletivas")

    else:
        dados['modo'] = 'atualizar'
        try:
            dados['message'] = menssagem_var['mensagem']
            menssagem_var['mensagem'] = ""
        except:
            dados['message'] = ""
        return render(request,'carrossel/carrossel.html',dados)