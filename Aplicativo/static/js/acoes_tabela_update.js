//função para quando o usuário clicar no campo que deseja atualizar redirecionar para a página de update 
let tabela = document.querySelector('table[id="tabela"]').dataset.user

function adicionar_linha(x){
    window.location.href = `/area-restrita/update/${tabela}/${x.id}`
}