from flask_restful import Resource, reqparse
from modules.CalculatorAPI.utils.util import ranged_type, normalize_path_params
from modules.CalculatorAPI.models.champions.kennen import Kennen

champion_attrib = reqparse.RequestParser()
champion_attrib.add_argument('champion_name', type=str, required=True,
                             help="Field 'champion_name' cannot be left ""blank.", location="args")
champion_attrib.add_argument('champion_level', type=ranged_type(int, 1, 18), location="args")
champion_attrib.add_argument('champion_q_skill_level', type=ranged_type(int, 0, 5), location="args")
champion_attrib.add_argument('champion_w_skill_level', type=ranged_type(int, 0, 5), location="args")
champion_attrib.add_argument('champion_e_skill_level', type=ranged_type(int, 0, 5), location="args")
champion_attrib.add_argument('champion_r_skill_level', type=ranged_type(int, 0, 5), location="args")
champion_attrib.add_argument('champion_items', type=str, location="args")

# enemy
enemy_champion_attrib = reqparse.RequestParser()
enemy_champion_attrib.add_argument('e_champion_name', type=str, required=True,
                                   help="Field 'enemy_champion_name' cannot be left blank.", location="args")
enemy_champion_attrib.add_argument('e_champion_level', type=ranged_type(int, 1, 18), location="args")
enemy_champion_attrib.add_argument('e_champion_q_skill_level', type=ranged_type(int, 0, 5), location="args")
enemy_champion_attrib.add_argument('e_champion_w_skill_level', type=ranged_type(int, 0, 5), location="args")
enemy_champion_attrib.add_argument('e_champion_e_skill_level', type=ranged_type(int, 0, 5), location="args")
enemy_champion_attrib.add_argument('e_champion_r_skill_level', type=ranged_type(int, 0, 5), location="args")
enemy_champion_attrib.add_argument('e_champion_items', type=str, location="args")


class CalculatorAPI(Resource):
    def get(self):
        # receive the params of champion in a variable and normalize them
        champion_data = champion_attrib.parse_args()
        champion_valid_data = {item: champion_data[item] for item in champion_data if champion_data[item] is not None}
        champion_params = normalize_path_params(**champion_valid_data)

        # receive the params of enemy champion in a variable and normalize them
        enemy_data = enemy_champion_attrib.parse_args()
        enemy_champion_valid_data = {item: enemy_data[item] for item in enemy_data if enemy_data[item] is not None}
        enemy_params = normalize_path_params(**enemy_champion_valid_data)

        champion = Kennen(**champion_params)

        enemy_champion = Kennen(**enemy_params)

        return champion.json()
