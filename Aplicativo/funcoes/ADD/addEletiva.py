from django.shortcuts import render
from ...forms import AddEletivaForm
from ...models import Eletivas
from ...views import excluir_imagem,menssagem_var,verificar_se_o_usuario_pode_realizar_a_acao_equisitada,checar_imagem_existente
from django.shortcuts import redirect
#função que adiciona as eletivas
def add_eletivas(request):
    #chama a função que verifica se o usuário está apto ou não à adicionar eletivas ou não
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
        return redirect("/")
    
    if request.method == 'POST':
        #chamando o form 
        form = AddEletivaForm(request.POST, request.FILES)
        if form.is_valid():
            #variável que armazena o nome da eletiva
            eletiva = form.cleaned_data.get('titulo')
            #variável que armazena a imagem de fundo da eletiva
            imagem = checar_imagem_existente(form.cleaned_data.get("imagem"),"img_eletivas",None)
            #variável que armazena a imagem dos professores da eletiva. Ele recebe o "request.FILES.get" porque  este campo não esta presente no form do django
            imagem_p = checar_imagem_existente(request.FILES.get("imagem_p"),"img_eletivas/img_professores_eletiva",None)
            #criando a nova eletiva
            new = Eletivas(titulo=eletiva,descricao=form.cleaned_data.get('descricao'),imagem=imagem,img_professores_eletiva=imagem_p,link=form.cleaned_data.get("link"))
            #salvando-a
            new.save()
            #redirecionando para a função que adiciona o professor responsável pela eletiva
            excluir_imagem("img_eletivas",Eletivas.objects.all().values())
            menssagem_var['mensagem'] = "Eletiva Adicionada!"
            return redirect("/area-restrita/add/professor")
    else:
        dados = {}
        #variável que retorna o form para o html
        dados['form'] = AddEletivaForm()
        dados['message'] = ''
        return render(request,'eletiva/addeletiva.html',dados)