from ...views import dados_universsais,menssagem_var
from ...models import CarrosselProfessores,Professores
from ..funcoes_sem_url.checar_imagem import checar_imagem_existente
from django.shortcuts import render, redirect
def add_professor_carrossel(request):
    dados = dados_universsais.copy()
    if dados['user'] != 'ADMIN':
        menssagem_var['mensagem'] = "Só o diretor pode adicionar professores ao carrossel"
        return redirect("/eletivas")
    if request.method == 'POST':
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')
        graduacao = request.POST.get('graduacao')
        descricao = request.POST.get('descricao')
        imagem = checar_imagem_existente(request.FILES.get('imagem'),'carrosselProfessores','cadastrar') 
        campo = CarrosselProfessores(nome=nome,idade=idade,graduacao=graduacao,descricao=descricao,imagem=imagem)
        campo.save()
        menssagem_var['mensagem'] = "Professor adicionado ao carrossel"
        return redirect(add_professor_carrossel)
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
        return render(request,'carrossel/carrossel.html',dados)
    #acabar de fazer o adicionar aqui
    