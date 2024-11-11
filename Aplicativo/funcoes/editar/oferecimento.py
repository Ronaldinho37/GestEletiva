from ...views import dados_universsais,menssagem_var
from ..funcoes_sem_url.excluir_imagem import excluir_imagem
from ..funcoes_sem_url.checar_imagem import checar_imagem_existente
from django.shortcuts import render, redirect
from ...models import OqueTemosaOferecer
def editar_oferecimento(request,id):
    if dados_universsais['user'] != 'ADMIN':
        menssagem_var['mensagem'] = 'Somente o ADMIN(diretor) pode editar os oferecimentos'
        return redirect("/")
    dados = {}
    try:
        oferecimento_a_ser_atualizado = OqueTemosaOferecer.objects.get(id=id)
    except:
        menssagem_var['mensagem'] = "Id não encontrado"
        return redirect("/")
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
    
        oferecimento_a_ser_atualizado.save()
        excluir_imagem('img_OqueTemosaOferecer',OqueTemosaOferecer.objects.all().values())
        menssagem_var['mensagem'] = "Oferecimento atualizado"
        return redirect("/")
    else:
        return render(request, 'OqueTemosaOferecer/editar_oferecimento.html', dados)