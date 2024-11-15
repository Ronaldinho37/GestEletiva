//funcão que adiciona os ids dos user a serem deletados
let users_a_serem_excluidos = []
let span = document.querySelector('span[id="numero_selecionados"]')
let tabela = document.querySelector('table[id="tabela"]').dataset.user
let id_do_user_logado = Number(document.querySelector('table[id="tabela"]').dataset.id_do_user_logado)
let modo = document.querySelector('div[id="table-py"]').dataset.modo
console.log(modo)

function adicionar_linha(x){
    if(users_a_serem_excluidos.includes(`${x.id}`) == false){
        if(id_do_user_logado == x.id){
            window.alert('Voçe não pode se auto deletar')
        } else {
            //adicona o id do user à lista de ids a serem deletados
            users_a_serem_excluidos.push(x.id)
            //atualiza o tamanho da lista que contém os ids no html
            span.innerText = users_a_serem_excluidos.length
            //adiciona uma borda vermelha
            x.style.border = "1px solid red"
            if(modo != 'deletar'){
                document.querySelector("input[id='ids']").value = users_a_serem_excluidos;
            }
        }
        
    } else {
        //retira a borda vermelha
        x.style.border = ""
        //retira o usuário da lista de ids 
        let u = users_a_serem_excluidos.filter(item => item !== x.id)
        //atualiza a lista de ids
        users_a_serem_excluidos = u
        //muda a quantidade de ids no HTML, de acordo com que o usuário vai clicando
        span.innerText = users_a_serem_excluidos.length
    }   
}
function adicionar_carrossel(){
    if(users_a_serem_excluidos.length != 0){
        document.querySelector('input[id="submit"]').click()
    }

}

function ir_para_o_site(){
    //se o tamanho da lista for menor que 1 é porque não tem nada na lista ainda
    if(users_a_serem_excluidos.length >= 1){
        window.location.href = `/area-restrita/deletar/${tabela}/${users_a_serem_excluidos}`
    } else {
        window.alert("Selecione pelo menos um usuário")
    }
   
}