import os
#esta função excluirá as imagens inutilizadas
#dir = Pasta que está localizado a imagem a ser excluída
#model = Valores do model django passado como parâmetro
def excluir_imagem(dir,model):
    #variável que guarda as imagens que estão sendo utilizadas
    imagens_usuarios = []
    try:
        #variável que guarda todas imagens da pasta media
        imagens_da_pasta_solicitada = os.listdir(f'{os.getcwd()}/media/{dir}')
    except:
        return
    #caso a pasta passada como parâmetro seja a 'pasta_da_velha_imagem' é necessário que se exclua a sub-pasta 'img_professores_eletiva', pois eu só preciso das imagens
    if dir == 'img_eletivas':
        imagens_da_pasta_solicitada.remove('img_professores_eletiva')
    #essa variável tem nome de 'coluna_da_vez' pois na maioria dos models o nome da coluna referente a imagem é 'imagem'
    #e em Eletivas o nome é 'img_professores_eletiva'
    coluna_da_vez = ''
    #esse if remove a imagem padrão da lista caso a pasta(dir) for 'img_eletivas/img_professores_eletiva'
    #e atribui a variável 'coluna_da_vez' o nome da coluna 'img_professores_eletiva'
    if dir == 'img_eletivas/img_professores_eletiva':
        imagens_da_pasta_solicitada.remove('Professorpadrao.jpg')
        coluna_da_vez += 'img_professores_eletiva'
    #como só é um model que usa um nome de coluna diferente então se o if acima for False será atribuído a variável 'coluna_da_vez' o valor 'imagem'   
    else:
        coluna_da_vez += 'imagem'
    #for que percorre o model possibilitando obter cada imagem usada no moedel
    for i in model:
        #if que atribui a variável 'imagens_usuarios' as imagens que estão sendo usadas
        if i[coluna_da_vez] != None and i[coluna_da_vez] not in imagens_usuarios:
            #ao ser adicionado uma imagem ela receberá o seguinte valor: pasta/imagem(pasta: para onde ele vai; imagem: a imagem)
            #porém como eu só quero a imagem, essa linha exclui o nome da pasta e adiciona somente o nome da imagem a variável 'imagens_usuarios'
            img = i[coluna_da_vez].replace(f'{dir}/','')
            imagens_usuarios.append(img)
    #for que percorre as imagens da pasta(dir)
    for i in imagens_da_pasta_solicitada:
        #se a imagem da pasta não esta em 'imagens_usuarios', então ela esta inutilizada portanto apague-a
        if i not in imagens_usuarios:
            os.remove(f'{os.getcwd()}/media/{dir}/{i}')     
    return