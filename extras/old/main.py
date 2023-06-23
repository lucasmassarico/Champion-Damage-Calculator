from extras.old.Data.Classes.useful import WikiPageRetriever, Url, urls
from extras.old.Data.Classes.champion import ChampionsStatusTransform, SkillsScrapperModel

items = WikiPageRetriever(url=urls["item_data"])
champions = ChampionsStatusTransform()
for champion in champions.return_champions():
    if not (champion == "Kled" or champion == "Mega Gnar"):
        wiki_champion = Url(champion=champion, base_url=urls["url_base"])
        # match champion:
        #    case 'Aatrox':
        #        skill_scrapper = Aatrox(url=wiki_champion)
        champion = SkillsScrapperModel(url=wiki_champion)
        print(champion)

print(champions)
