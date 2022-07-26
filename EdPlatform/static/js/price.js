function doprice() {
    var list = document.getElementsByClassName('price');
    for (i=0; i<list.length; i++){
        list[i].innerHTML = document.getElementsByClassName('price')[i].textContent.replace(',', ' ').replace(',', ' ');
        }
    }
