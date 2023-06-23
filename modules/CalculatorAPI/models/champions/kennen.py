from modules.MongoAPI.models.champions.champion import ChampionModel
from modules.CalculatorAPI.utils.util import calculate_stats


class DamageReceived:
    def physical_damage(self):
        pass

    @staticmethod
    def magical_damage(skill_damage, magic_resistance):
        pass


class Kennen(DamageReceived):
    def __init__(self,
                 champion_name,
                 champion_level,
                 champion_items,
                 champion_q_skill_level,
                 champion_w_skill_level,
                 champion_e_skill_level,
                 champion_r_skill_level):
        self.champion_name = champion_name
        self.champion_level = champion_level
        self.champion_items = champion_items
        self.q_skill_level = champion_q_skill_level
        self.w_skill_level = champion_w_skill_level
        self.e_skill_level = champion_e_skill_level
        self.r_skill_level = champion_r_skill_level
        self._db_champion = ChampionModel.find_champion_by_name(self.champion_name)
        self.stats = self._calculate_champion_stats()
        self.skills = self._get_skills(self.q_skill_level, self.w_skill_level, self.e_skill_level, self.r_skill_level)

    def json(self):
        return {
            "stats": self.stats,
            "skills": self.skills
        }

    def _calculate_champion_stats(self):
        return calculate_stats(self._db_champion.get('stats'), self.champion_level)

    def calculate_instance_skill_damage(self, skill_level, leveling):
        flat_damage = 0
        scaling = 0
        for modifier in leveling['modifiers']:
            # verifica se é scaling ou flat damage
            if modifier["units"][skill_level] == "":
                flat_damage += modifier["values"][skill_level]
            elif modifier["units"][skill_level]:
                match modifier["units"][skill_level]:
                    case "% AP":
                        scaling += (modifier["values"][skill_level] / 100) * self.stats['abilityPower']
                    case "% AD":
                        scaling += (modifier["values"][skill_level] / 100) * self.stats['attackDamage']
                    case "% HP MAX":
                        pass
        return flat_damage + scaling

    def _get_skills(self, q_skill_level, w_skill_level, e_skill_level, r_skill_level):
        # Q
        q_skill = self._db_champion['abilities']['Q']
        q_skill_effects = q_skill[0]['effects'][0]['leveling'][0]
        q_skill_damage = self.calculate_instance_skill_damage(q_skill_level, q_skill_effects)

        # W
        w_skill = self._db_champion['abilities']['W']
        w_skill_effects_active = w_skill[0]['effects'][1]['leveling'][0]
        w_skill_damage_active = self.calculate_instance_skill_damage(w_skill_level, w_skill_effects_active)
        w_skill_total_damage = w_skill_damage_active

        # E
        e_skill = self._db_champion['abilities']['E']
        e_skill_effects = e_skill[0]['effects'][0]['leveling'][0]
        e_skill_damage = self.calculate_instance_skill_damage(e_skill_level, e_skill_effects)

        # R
        r_skill = self._db_champion['abilities']['R']
        r_skill_effects = r_skill[0]['effects'][2]['leveling'][0]
        r_skill_damage = self.calculate_instance_skill_damage(r_skill_level, r_skill_effects)

        return {
            "q": q_skill_damage,
            "w": w_skill_total_damage,
            "e": e_skill_damage,
            "r": r_skill_damage
        }
