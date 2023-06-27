// Obtenha todas as spans com a classe "ability"
    var abilities = document.querySelectorAll('.ability');

    // Adicione um ouvinte de evento de clique a cada span
    abilities.forEach(function(ability) {
      ability.addEventListener('click', function() {
        var infoTarget = this.getAttribute('data-info');
        var infoDiv = document.querySelector('.' + infoTarget);

        // Remova a classe "active" de todas as divs de informações
        var allInfoDivs = document.querySelectorAll('.ability-info > div');
        var abilityInfo = document.querySelector('.ability-info');
        allInfoDivs.forEach(function(div) {
          abilityInfo.style.display = 'flex';
          div.classList.remove('active');
        });

        // Adicione a classe "active" à div de informações correspondente
        infoDiv.classList.add('active');
      });
    });