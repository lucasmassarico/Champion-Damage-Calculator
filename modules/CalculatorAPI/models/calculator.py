from modules.MongoAPI.models.champions.champion import ChampionModel
from modules.CalculatorAPI.utils.util import calculate_stats


class CalculatorModel:
    def __init__(self, champion_name, champion_level, champion_items):
        self._champion_name = champion_name
        self._champion_level = champion_level
        self._champion_items = champion_items
        self._champion_stats = self._calculate_champion_stats()

    def _calculate_champion_stats(self):
        db_champion = ChampionModel.find_champion_by_name(self._champion_name)
        return calculate_stats(db_champion.get('stats'), self._champion_level)

    def _get_skills(self):
        pass

    def _match_case(self, champion_name, stats):
        dictionary_champions_name = {
            "Aatrox": self._aatrox()
        }
