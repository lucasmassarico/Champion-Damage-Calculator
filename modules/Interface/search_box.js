const searchInput = document.getElementById('search-input');
const champions = document.querySelectorAll('.icon-container div');

searchInput.addEventListener('input', function() {
    const searchText = searchInput.value.toLowerCase();

    champions.forEach(function(champion) {
        const championName = champion.querySelector('span').textContent.toLowerCase();
        const championMatchesSearch = championName.includes(searchText);

        if (championMatchesSearch) {
            champion.style.display = 'flex';
        } else {
            champion.style.display = 'none';
        }
    });
});
