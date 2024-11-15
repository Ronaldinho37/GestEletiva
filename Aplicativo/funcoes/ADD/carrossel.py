from ...views import dados_universsais,menssagem_var
from ...models import CarrosselProfessores,Professores
from ..funcoes_sem_url.checar_imagem import checar_imagem_existente
from django.shortcuts import render, redirect
def add_professor_carrossel(request):
    dados = dados_universsais.copy()
    carrossel = CarrosselProfessores.objects.get(id=1)
    if dados['user'] != 'ADMIN':
        menssagem_var['mensagem'] = "Só o diretor pode adicionar professores ao carrossel"
        return redirect("/eletivas")
    if request.method == 'POST':
        ids = request.POST.get('ids')
        try:
            todos_ids = f'{carrossel.ids},{ids}'
            todos_ids = todos_ids.split(',')
            ordem_crescente = []
            for i in todos_ids:
                if i not in ordem_crescente:
                    ordem_crescente.append(i)
            ordem_crescente.sort()
            carrossel.ids = ','.join(ordem_crescente)           
            carrossel.save()
        except:
            carrossel = CarrosselProfessores(id=1,ids=ids)
            carrossel.save()
        menssagem_var['mensagem'] = "Professor adicionado ao carrossel!"
        return redirect("/eletivas")
        
    else:
        dados['usuarios'] = Professores.objects.filter(tutor=True,professor=True).values()
        dados['modo'] = 'adicionarcarrossel'
        try:
            dados['message'] = menssagem_var['mensagem']
            menssagem_var['mensagem'] = ""
        except:
            dados['message'] = ""
        dados['tabela_user_passado_como_parametro'] = "professor"
        dados['modo'] = 'carrossel'
        dados['usuarios'] = Professores.objects.filter(professor=True)
        for i in carrossel.ids.split(','):
            dados['usuarios'] = dados['usuarios'].exclude(id=int(i))    
        return render(request,'carrossel/carrossel.html',dados)
    #acabar de fazer o adicionar aqui
    