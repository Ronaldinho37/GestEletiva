from ...models import Anuncio
from ...forms import AnuncioForm
from ...views import menssagem_var
from ..funcoes_sem_url.checar_imagem import checar_imagem_existente
from ..funcoes_sem_url.excluir_imagem import excluir_imagem
from ..funcoes_sem_url.acao_requisitada import verificar_se_o_usuario_pode_realizar_a_acao_equisitada
from django.shortcuts import render, redirect
#função que edita e se ele não existir cria o aviso
def editar_aviso(request,id):
    #verificando se a página pode funcionar
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
        return redirect("/")
    #como são só 2 avisos então não faz sentido o id passado na url ser maior que 2
    if id <= 2 and id > 0:
        #tente pegar o aviso, se não der é porque ele não existe, então crie-o(são criados os avisos de id 1 e 2)
        try:
            anuncio_a_ser_atualizado = Anuncio.objects.get(id=id)
        except:
            #número de avisos adicionados
            anuncios = 1
            #enquato 'anuncios' for menor ou igual a 2(limite de avisos)
            while anuncios <= 2:
                #crie avisos com quaisquer valores(exceto o id)
                anuncio_a_ser_cadastrado = Anuncio(id=anuncios,titulo='titulo',descricao='descricao',imagem=checar_imagem_existente(None,'img_anuncio',None),link='https://www.google.com.br')
                #salve-os
                anuncio_a_ser_cadastrado.save()
                #atribua 1 à variável 'anuncios', pois 1 aviso foi adicionado 
                anuncios += 1
            #pegue o aviso com o respectivo id
            anuncio_a_ser_atualizado = Anuncio.objects.get(id=id)
        #todos os valores antigos do aviso
        titulo_antigo = anuncio_a_ser_atualizado.titulo
        descricao_antiga = anuncio_a_ser_atualizado.descricao
        imagem_antiga = anuncio_a_ser_atualizado.imagem
        link_antigo = anuncio_a_ser_atualizado.link
        #Pega valores presentes no form
        if request.method == 'POST':
            #todos os novos valores do aviso
            titulo = request.POST.get('titulo')
            descricao = request.POST.get('descricao')
            imagem = request.FILES.get('imagem')
            link = request.POST.get('link')
            #esta variavel contem todos os valores que forem inseridos  
            campos_novos = [titulo,descricao,imagem,link]
            #esta variavel contem todos os valores antigos do aviso
            campos_antigos = [titulo_antigo,descricao_antiga,imagem_antiga,link_antigo]
            #variável que representa em qual campo o loop for esta, ex: 0=titulo_antigo,1=descricao_antiga...
            tam = 0
            #for usado para checar se algum dos campos do anuncio e igual ao inserido na variavel campos novos
            for i in campos_novos:
                #somente se for diferente adicione. O campo da imagem é só se for diferente de None
                if tam == 0 and i != campos_antigos[tam]:
                    anuncio_a_ser_atualizado.titulo = i
                elif tam == 1 and i != campos_antigos[tam]:
                    anuncio_a_ser_atualizado.descricao = i
                elif tam == 2 and i != None:
                    #checa se ja existe uma imagem na variavel
                    imagem_final = checar_imagem_existente(imagem,'img_anuncio',None)
                    anuncio_a_ser_atualizado.imagem = imagem_final
                elif tam == 3 and i != campos_antigos[tam]:
                    anuncio_a_ser_atualizado.link = i
                tam += 1
            #salvando as alterações efetuadas
            anuncio_a_ser_atualizado.save()
            #chamando a função que exclui a imagem se ela não esta mais sendo usada
            excluir_imagem('img_anuncio',Anuncio.objects.all().values())
            menssagem_var['mensagem'] = "Aviso alterado com sucesso"
            return redirect("/")
        else:
            dados = {}
            #MODIFICAR AQUI#
            dados['form'] = AnuncioForm()
            dados['titulo'] = anuncio_a_ser_atualizado.titulo
            dados['descricao'] = anuncio_a_ser_atualizado.descricao
            dados['imagem'] = anuncio_a_ser_atualizado.imagem
            dados['link'] = anuncio_a_ser_atualizado.link
            return render(request, 'anuncio/addanuncio.html', dados)
    #se o id for diferente de 1 ou 2 saía daqui
    else:
        return redirect("/")