let users_a_serem_excluidos = []
let span = document.querySelector('span[id="numero_selecionados"]')
let tabela = document.querySelector('table[id="tabela"]').dataset.user
let id_do_user_logado = Number(document.querySelector('table[id="tabela"]').dataset.id_do_user_logado)
let modo = document.querySelector('div[id="table-py"]').dataset.modo


function adicionar_linha(x){
    if(users_a_serem_excluidos.includes(`${x.id}`) == false){
        if(id_do_user_logado == x.id){
            window.alert('Voçe não pode se auto deletar')
        } else {
            users_a_serem_excluidos.push(x.id)
            span.innerText = users_a_serem_excluidos.length
            x.style.border = "1px solid red"
        }
        
    } else {
        x.style.border = ""
        let u = users_a_serem_excluidos.filter(item => item !== x.id)
        users_a_serem_excluidos = u
        span.innerText = users_a_serem_excluidos.length
    }
    if(modo == 'adicionarcarrossel'){
        document.querySelector('input[name="ids"]').value = users_a_serem_excluidos
    }
   
}

function ir_para_o_site(){
    if(users_a_serem_excluidos.length >= 1){
        window.location.href = `/area-restrita/deletar/${tabela}/${users_a_serem_excluidos}`
    } else {
        window.alert("Selecione pelo menos um usuário")
    }
   
}