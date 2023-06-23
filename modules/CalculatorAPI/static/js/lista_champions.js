function update() {
    var select = document.getElementById('myList');
    var value = select.options[select.selectedIndex].value;
    console.log(value);


}
update();