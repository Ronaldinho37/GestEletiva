function ValidarForm(){
    let checboxes = document.querySelectorAll('input[type="checkbox"]') 
    let inputs = ['nome','senha','email']
    for(i of inputs){
        let input = document.querySelector(`input[id="${i}"]`)
        if(input.value == ''){
            return false
        }
    }
    for(i of checboxes){
        if(i.checked == true){
            document.querySelector('input[name="link_antigoA"]').value = sessionStorage.getItem('link');
            return true
        }
    }
    window.alert('Marque ao menos uma ação que o admin possa realizar!')
    return false
}
