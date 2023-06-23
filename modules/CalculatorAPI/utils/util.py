import argparse


def ranged_type(value_type, min_value, max_value):
    """
    Return function handle of an argument type function for ArgumentParser checking a range:
        min_value <= arg <= max_value

    Parameters
    ----------
    value_type  - value-type to convert arg to
    min_value   - minimum acceptable argument
    max_value   - maximum acceptable argument

    Returns
    -------
    function handle of an argument type function for ArgumentParser


    Usage
    -----
        ranged_type(float, 0.0, 1.0)
    """

    def range_checker(arg: str):
        try:
            f = value_type(arg)
        except ValueError:
            raise argparse.ArgumentTypeError(f'must be a valid {value_type}')
        if f < min_value or f > max_value:
            raise argparse.ArgumentTypeError(f'must be within [{min_value}, {max_value}]')
        return f

    return range_checker


# Increasing Statistics formula
def increasing_champion_statistic(base_statistic, growth_statistic, level):
    """
    Increase a growth statistics of champions
    :param base_statistic: int,
    :param growth_statistic: float,
    :param level: int,
    :return: float
    """
    return round(base_statistic + growth_statistic * (level - 1) * (0.7025 + 0.0175 * (level - 1)), 2)


def normalize_path_params(champion_name=None,
                          champion_level=1,
                          champion_q_skill_level=0,
                          champion_w_skill_level=0,
                          champion_e_skill_level=0,
                          champion_r_skill_level=0,
                          champion_items=None,
                          e_champion_name=None,
                          e_champion_level=1,
                          e_champion_q_skill_level=0,
                          e_champion_w_skill_level=0,
                          e_champion_e_skill_level=0,
                          e_champion_r_skill_level=0,
                          e_champion_items=None):
    """
    Normalize params to get method of calculator

    :param champion_name: string,
    :param champion_level: int,
    :param champion_q_skill_level: int,
    :param champion_w_skill_level: int,
    :param champion_e_skill_level: int,
    :param champion_r_skill_level: int,
    :param champion_items: string,

    :param e_champion_name: string,
    :param e_champion_level: int,
    :param e_champion_q_skill_level: int,
    :param e_champion_w_skill_level: int,
    :param e_champion_e_skill_level: int,
    :param e_champion_r_skill_level: int,
    :param e_champion_items: string,
    :return: dict
    """
    if champion_name:
        return {
            'champion_name': champion_name.capitalize(),
            'champion_level': champion_level,
            'champion_q_skill_level': champion_q_skill_level,
            'champion_w_skill_level': champion_w_skill_level,
            'champion_e_skill_level': champion_e_skill_level,
            'champion_r_skill_level': champion_r_skill_level,
            'champion_items': champion_items,
        }
    elif e_champion_name:
        return {
            'champion_name': e_champion_name.capitalize(),
            'champion_level': e_champion_level,
            'champion_q_skill_level': e_champion_q_skill_level,
            'champion_w_skill_level': e_champion_w_skill_level,
            'champion_e_skill_level': e_champion_e_skill_level,
            'champion_r_skill_level': e_champion_r_skill_level,
            'champion_items': e_champion_items
        }

    # return {
    #     'champion_name': champion_name,
    #     'champion_level': champion_level,
    #     'champion_items': champion_items,
    #     'e_champion_name': e_champion_name,
    #     'e_champion_level': e_champion_level,
    #     'e_champion_items': e_champion_items
    # }


def calculate_stats(all_stats, level):
    """
        This function get 
        ---------->
        patterns in stats from db_champion:
        health, healthRegen, mana, manaRegen, armor, magicResistance,
        attackDamage, movespeed, attackSpeed, attackRange
        ---------->
        pattern in stats['stats_type']:
        flat, perLevel
    """
    stats_to_get = ["health", "healthRegen", "mana", "manaRegen", "armor", "magicResistance", "attackDamage",
                    "movespeed", "attackSpeed", "attackRange"]

    calculated_stats = dict()
    for stats in stats_to_get:
        stats_type_flat = all_stats[stats].get("flat")
        stats_type_per_level = all_stats[stats].get("perLevel")

        if stats == "attackSpeed":
            stats_type_per_level = stats_type_per_level / 100

        calculated_stats[stats] = increasing_champion_statistic(base_statistic=stats_type_flat,
                                                                growth_statistic=stats_type_per_level,
                                                                level=level)
        if stats == "attackDamage":
            calculated_stats['baseDamage'] = calculated_stats[stats]

    calculated_stats['abilityPower'] = 0

    return calculated_stats
