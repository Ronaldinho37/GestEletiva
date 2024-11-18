let buttons = document.querySelectorAll('.nova_aba');
function Abrir_nova_aba(url){
    var win = window.open(url, '_blank');
    win.focus();
}
buttons.forEach((x)=>{
    x.addEventListener('click',function (){
       
        Abrir_nova_aba(x.dataset.link)
    })
})