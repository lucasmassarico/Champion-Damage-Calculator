import os
import json
from utils import utils
from modules.MongoAPI.models.champions.champion import ChampionModel
from modules.CelestialCodex.lolstaticdata.champions.__main__ import create_champions_json


def update_champions_bd():
    """
        This method update collections 'champions' in database with CelestialCodex'
        Returns:
            String if success or not
    """
    # check_lol_version = utils.get_latest_patch_version()

    # # get Aatrox in BD and verify if latest patch of game is the same of bd
    # first_champion = ChampionModel.find_champion_by_name("Aatrox")

    # url_pattern = r'/(\d+\.\d+\.\d+)/'
    # champion_icon = first_champion.get("icon")

    # latest_patch_in_bd = utils.get_patch_version_in_url(
    #     champion_icon, url_pattern)

    # if latest_patch_in_bd == check_lol_version:
    #     print("BD is update")
    
    # Create JSON's of Each Champion and Super JSON with all champions
    create_champions_json()

    # Get archives name in modules/CelestialCodex/champions/
    champions_directory = f"{utils.get_father_directory_of_project()}/modules/CelestialCodex/champions"
    if not os.path.exists(champions_directory):
        print(f"Folder {champions_directory} not exists.\nExiting ;(")
        exit(1)

    archive_names = sorted(os.listdir(champions_directory))
    for name in archive_names:
        file_path = os.path.join(champions_directory, name)
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    file_contents = file.read()
                    champion_json = json.loads(file_contents)
                    champion_kwargs = champion_json.values()
                    champion = ChampionModel(*champion_kwargs)
                    champion.update_champion_by_id()
            except IOError as error:
                print(f"An error occurred trying open file {file_path}: {error}")
        else:
            print(f"{file_path} not is archive.")


if __name__ == "__main__":
    update_champions_bd()
