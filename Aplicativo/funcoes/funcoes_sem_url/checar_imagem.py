import os
from PIL import Image
#esta função serve para verificar se a imagem a ser adicionada é existente se não for a adicionará 
#se for então será adicionado o caminho referente a ela
def checar_imagem_existente(imagem,pasta,acao):
    #este if adiciona as imagens padrões caso a variável "imagem" seja igual a None 
    if imagem == None:
        #caso seja uma imagem da dupla de professores
        if pasta == 'img_eletivas/img_professores_eletiva':
            return f'{pasta}/Professorpadrao.jpg'
        #caso seja um user
        else:
            return 'img_fixas/anonimo.png'
    #se chegou até aqui é porque nenhum dos ifs acima foi verdadeiro, logo a imagem inserida não é igual a None
    #o único jeito que consegui verificar se a imagem não é igual às demais foi transformando-as em bytes
    #esta variável recebe os bytes equivalentes a imagem inserida
    nova_imagem = Image.open(imagem).tobytes("xbm", "rgb")
    #esse try server para pegar todas as imagens da pasta passada como parâmetro
    #se a pasta não existir então irá retornar a imagem
    try:
        #variável que contém todos os itens da pasta requisitada, em forma de lista
        pasta_da_velha_imagem = os.listdir(f'{os.getcwd()}/media/{pasta}')
    except:
      
        return imagem
    #essa variável serve para eu ter um controle do que esta acontecendo, mais a frente ele dirá se eu tenho ou não de adicionar a imagem
    tam = 0
    #for que percorre a variável "pasta_da_velha_imagem"
    for e in pasta_da_velha_imagem:
        #esse if é importante pois "img_professores_eletiva" não é uma imagem mas sim uma pasta
        if e !=  'img_professores_eletiva':
            #essa variável receberá todas as imagens da pasta em forma de bytes, uma por vez 
            imagem_da_pasta = Image.open(f'{os.getcwd()}/media/{pasta}/{e}').tobytes("xbm", "rgb")
            #caso a "imagem_da_pasta" for igual a "nova_imagem" esse if retornará o caminho referente a mesma
            if nova_imagem == imagem_da_pasta:
                return f'{pasta}/{e}'
        #se as imagens não forem iguais então será agregado valor à variável de controle
        tam += 1
    #se a variável de controle for igual a 0 é porque nenhuma das imagens é igual a imagem inserida pelo user
    #se a quantidade de itens da variável "pasta_da_velha_imagem" for igual a 0 é porque não tem imagem na pasta
    #logo se ambas ou apenas uma for verdadeira o código retornará a imagem 
    if tam != 0 or len(pasta_da_velha_imagem) == 0:
        return imagem