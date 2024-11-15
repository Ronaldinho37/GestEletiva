from ...views import dados_universsais, menssagem_var
from django.shortcuts import render, redirect
from ...models import CarrosselProfessores
from ..funcoes_sem_url.excluir_imagem import excluir_imagem
def deletar_carrossel(request,id):
    dados = dados_universsais.copy()
    if dados['user'] != 'ADMIN':
        menssagem_var['mensagem'] = "Só o diretor pode deletar o carrossel"
        return redirect("/eletivas")
    if request.method == 'POST':
        sim = request.POST.get('sim')
        if sim == 'on':
            try:
                carrossel = CarrosselProfessores.objects.get(id=1)
                ids_carrossel = carrossel.ids.split(',')
                ids_finais = []
                for i in ids_carrossel:
                    if i != f'{id}':
                        ids_finais.append(i)
                carrossel.ids = ','.join(ids_finais)
                carrossel.save()
                menssagem_var['mensagem'] = 'Carrossel deletado'
            except:
                menssagem_var['mensagem'] = 'Id não identificado'
        return redirect("/eletivas")
    else:
        dados['tam_lista_id'] = 1
        try:
            dados['message'] = menssagem_var['mensagem']
            menssagem_var['mensagem'] = ""
        except:
            dados['message'] = ""
        return render(request, 'deletar/deletar_com_ids.html',dados)