from ..views import dados_universsais,menssagem_var,para_onde_vou
from django.contrib.auth import logout
#função que desloga o usuário
def logout_viwes(request):
    if request.method == "POST":
        user = request.session['user'] 
        #o admin supremo(ADMIN) é o único que foi criado como um user no django e por isso ele recebe um 
        #tratamento diferente dos demais, a função logout() é própria do Django ela server para deslogar o user que esta logado
        if user == 'ADMIN':
            logout(request)
        #se o usuário for um admin e quer deslogar-se então primeiro eu apago as sessions que comtém os valores 
        #das ações que ele pode realizar 
        elif user == 'admin':
            del request.session['lista_de_acoes']

        #por conseguinte eu limpo os valores da variável dos dados universais, pois ela guarda valores referentes
        # ao usuário e já que ele não está mais logado eu não preciso mais delas 
        dados_universsais.clear()
        #definindo o session 'user' como None, desta maneira o código saberá se o usuário está logado ou não
        request.session['user'] = None
        menssagem_var['mensagem'] = "Deslogado com sucesso!"
        link = request.POST.get('link_antigo')
        return para_onde_vou(request,link)