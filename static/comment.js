var field = document.querySelector('textarea');
var backup = field.getAttribute('placeholder');
var btn = document.querySelector('.btn');
var clear = document.getElementById('clear');

field.onfocus = function() {
    this.setAttribute('placeholder', '')
}

field.onblur = function() {
    this.setAttribute('placeholder', '')
}

clear.onclick = function() {
    btn.getElementsByClassName.display= 'none'
    field.value = ''
}