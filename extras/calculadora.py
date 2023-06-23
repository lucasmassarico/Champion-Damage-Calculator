from pymongo import MongoClient

username = "lucasmassarico1"
password = "niih050299"
connection_string = f'mongodb+srv://{username}:{password}@cluster.5ougas6.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(connection_string)
db = client['champion_calculator']
champion_collection = db['champions']


def increasing_statistics_champion(base_statistic, growth_statistic, level):
    return round(base_statistic + growth_statistic * (level - 1) * (0.7025 + 0.0175 * (level - 1)), 2)

#xD
champion_to_find = "Viktor"

champion = champion_collection.find_one({"name": champion_to_find})

# champions stats
champion_level = 10
champion_ability_power = 135
stats = champion['stats']

# formula = base + growth_statistic * (level - 1) * (0.7025 + 0.0175 * (level - 1)) ---> usada para qualquer calculo
# calculo ad
champion_flat_ad = stats['attackDamage']['flat']
champion_ad_per_level = stats['attackDamage']['perLevel']
# champion_ad = champion_flat_ad + champion_ad_per_level * (champion_level-1) * (0.7025 + 0.0175 * (champion_level - 1))
champion_ad = increasing_statistics_champion(
    champion_flat_ad, champion_ad_per_level, champion_level)

# calculo hp
champion_flat_hp = stats['health']['flat']
champion_hp_per_level = stats['health']['perLevel']
champion_health = increasing_statistics_champion(
    champion_flat_hp, champion_hp_per_level, champion_level)

# calculo mana
champion_flat_mana = stats['mana']['flat']
champion_mana_per_level = stats['mana']['perLevel']
champion_mana = increasing_statistics_champion(
    champion_flat_mana, champion_mana_per_level, champion_level)

# calculo armor
champion_flat_armor = stats['armor']['flat']
champion_armor_per_level = stats['armor']['perLevel']
champion_armor = increasing_statistics_champion(
    champion_flat_armor, champion_armor_per_level, champion_level)

# calculo_mr
champion_flat_mr = stats['magicResistance']['flat']
champion_mr_per_level = stats['magicResistance']['perLevel']
champion_mr = increasing_statistics_champion(
    champion_flat_mr, champion_mr_per_level, champion_level)

# calculo_atk_speed
champion_flat_atkspeed = stats['attackSpeed']['flat']
champion_atkspeed_per_level = stats['attackSpeed']['perLevel'] / 100
champion_atkspeed = increasing_statistics_champion(
    champion_flat_atkspeed, champion_atkspeed_per_level, champion_level)


print("AD: ", champion_ad)
print("HEALTH: ", champion_health)
print("MANA: ", champion_mana)
print("ARMOR: ", champion_armor)
print("MR: ", champion_mr)
bonus_as = round(champion_atkspeed_per_level * (champion_level - 1)
                 * (0.7025 + 0.0175 * (champion_level - 1)) * 100, 2)
print(f"BONUS AS: {bonus_as}%")
print("ATK SPEED: ", champion_atkspeed)
