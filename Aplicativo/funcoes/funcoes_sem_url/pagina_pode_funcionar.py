from ...models import PaginasUtilizaveis
from ...views import menssagem_var
def ver_se_a_pagina_pode_funcionar(pagina,dados):
    #false: não saía
    #true: saía
    #tente pegar os valores do object
    try:
        paginaModels = PaginasUtilizaveis.objects.values().get(id=1)
    #se não conseguir é porque não existe, então crie-o
    except:
        p1 = PaginasUtilizaveis(tutoria=True,eletiva=True,index=True,sobre=True)
        p1.save()
        return False 
    #pegua o valor referente a página passada como parâmetro, se for diferente de true é porque ela não pode ser utilizada 
    if paginaModels[f'{pagina}'] != True:
        dados['message'] = menssagem_var['mensagem']
        menssagem_var['mensagem'] = ""
        return True
    else:
        return False