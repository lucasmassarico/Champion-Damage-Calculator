window.addEventListener('DOMContentLoaded', function() {
    var championIcons = document.querySelectorAll('.icon-container img');
    var championContainer = document.querySelector('.y-champion-container-img');

    championIcons.forEach(function(icon) {
        icon.addEventListener('click', function() {
            var championName = icon.alt;
            var championImage = icon.src;

            var championContent = '<img src="' + championImage + '" alt="' + championName + '">';
            championContainer.innerHTML = championContent;
        });
    });
});

const championImages = document.querySelectorAll('.icon-container img');
const yChampionContainer = document.querySelector('.y-champion-container');
const yChampionContainerAbilities = document.querySelector('.y-champion-abilities');


championImages.forEach(function(image) {
    image.addEventListener('click', function() {
        yChampionContainer.style.display = 'flex';
        yChampionContainerAbilities.style.display = 'flex';
    });
});
