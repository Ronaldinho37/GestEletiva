from ...views import dados_universsais
def definir_user(request):
       #if que verifica se o ADMIN já estava logado
    if request.user.is_authenticated:
        request.session['user'] = 'ADMIN'
        request.session['nome_user_logado'] = ''
        request.session['senha_user_logado'] = ''
 
    dados = {}
    #como a session do Django dura enquanto o navegador estiver aberto(eu abilitei para isso) 
    #quando o usuário abrir o site pela primeira vez vai dar erro, por isso esse try
    #tente pegar essa session, se ela não existir então a crie definindo-a como None ou seja nenhum usuário por enquanto
    try:
        dados['user'] = request.session['user']
    except:
        request.session['user'] = None
        dados['user'] = request.session['user']
    if dados_universsais != dados and dados['user'] != None:
        #caso o user logado seja um admin precisarei da senha e do nome dele, para impedir que ele se auto atualize ou delete
        dados['nome_user_logado'] = request.session['nome_user_logado']
        dados['senha_user_logado'] = request.session['senha_user_logado']
        #caso o usuário for um admin então eu preciso de uma variável com todas as ações que ele pode realizar
        if dados['user'] == 'admin':
            dados['lista_de_acoes'] = request.session['lista_de_acoes']
    #atualizando a variável dos dados universsais para que eu possa acessar os valores adicionados de outras fuções
    dados_universsais.update(dados)
    return dados