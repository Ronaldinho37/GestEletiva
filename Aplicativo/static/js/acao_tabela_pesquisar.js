//função que faz a pesquisa de caractere dentre os valores da tabela 
function pesquisar(x){
    let coluna = document.querySelector('select[id="coluna"]').value
    let todos_valore = ""
    if(coluna != "id"){
        todos_valore = document.querySelectorAll(`td[class="${coluna}"]`)
    } else {
        todos_valore = document.querySelectorAll(`th[class="${coluna}"]`)
    }
    
    for(i of todos_valore){
        let texto_linhas = i.innerText.toLowerCase()
        let texto_input = x.value.toLowerCase()

        if(texto_linhas.includes(texto_input)){
            document.getElementById(i.dataset.id).style.display = ""
        } else {
            document.getElementById(i.dataset.id).style.display = "none"
        }
    }
    
}
