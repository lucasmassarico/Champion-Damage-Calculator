from utils import utils
from modules.MongoAPI.models.champions.champion import ChampionModel


check_lol_version = utils.get_latest_patch_version()

# get Aatrox in BD
first_champion = ChampionModel.find_champion_by_name("Aatrox")


url_pattern = r'/(\d+\.\d+\.\d+)/'
champion_icon = first_champion.get("icon")

latest_patch_in_bd = utils.get_patch_version_in_url(champion_icon, url_pattern)

if latest_patch_in_bd == check_lol_version:
    print("BD is update")
else:


