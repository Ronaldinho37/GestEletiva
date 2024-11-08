from ...views import dados_universsais, menssagem_var
from django.shortcuts import render, redirect
from ...models import OqueTemosaOferecer
from ..funcoes_sem_url.checar_imagem import checar_imagem_existente
def add_OqueTemosaOferecer(request):
    if dados_universsais['user'] != 'ADMIN':
        menssagem_var['mensagem'] = 'Somente o ADMIN(diretor) pode adicionar os oferecimentos'
        return redirect("/")
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        imagem = checar_imagem_existente(request.FILES.get('imagem'),'img_OqueTemosaOferecer','cadastrar')
        descricao = request.POST.get('descricao')
        link = request.POST.get('link')
        titulo_link = request.POST.get('titulo_link')

        novo_oferecimento = OqueTemosaOferecer(titulo=titulo,imagem=imagem,descricao=descricao,link=link,titulo_do_link=titulo_link)
        novo_oferecimento.save()
        menssagem_var['mensagem'] = "Oferecimento adicionado"
        return redirect("/")
    else:
        return render(request,'OqueTemosaOferecer/add_oferecimentos.html')