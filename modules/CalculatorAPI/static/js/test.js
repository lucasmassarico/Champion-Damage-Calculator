var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    var response = JSON.parse(this.responseText);
    var championList = document.getElementById("champion-list");
    var list = document.createElement("ul");
    for (var champ in response) {
        console.log('uii')
        var listItem = document.createElement("li");
        var champName = document.createTextNode(champ + " - level " + response[champ].level);
        var champStatsList = document.createElement("ul");
        for (var stat in response[champ].stats) {
            var champStat = document.createElement("li");
            var statName = document.createTextNode(stat + ": " + response[champ].stats[stat]);
            champStat.appendChild(statName);
            champStatsList.appendChild(champStat);
        }
        listItem.appendChild(champName);
        listItem.appendChild(champStatsList);
        list.appendChild(listItem);
    }
    championList.appendChild(list);
  }
};

xhttp.open("GET", "http://127.0.0.1:5998/calculator?champion_name=Aatrox&champion_level=18&e_champion_name=Ahri&e_champion_level=18", true);
xhttp.send();
