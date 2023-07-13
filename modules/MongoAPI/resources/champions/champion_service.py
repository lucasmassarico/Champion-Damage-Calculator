from modules.MongoAPI.resources.service_utils import get_dict_content_from_endpoints, pop_items_from_dict, login_in_mongo_api, put_method_to_api


def update_champions_in_bd():
    """
        This method update collections 'champions' in database with meraki endpoint 'champions.json'
        It uses two endpoint from MongoAPI:
            POST /login: to generate a token
            PUT /champions/{champions_id}: to insert/update champion in DB
        Returns:
            Nothing
    """
    from modules.MongoAPI.resources.service_config import champions_meraki_endpoint

    data = get_dict_content_from_endpoints(champions_meraki_endpoint)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid value of data. Data need to be a dict, but it is a {type(data)}.")

    total_champions = 0
    counter_inserted_champions = 0
    counter_not_inserted_champions = 0

    for champion in data.values():
        total_champions += 1

        # this method pop unnecessary items from 'champion'
        # pop_items_from_dict accept numerous params to pop
        # DROP FROM MERAKI: [stats]: aramDamageTaken, aramDamageDealt, aramHealing, aramShielding, urfDamageTaken
        # urfDamageDealt, urfHealing, urfShielding
        pop_items_from_dict(champion['stats'],
                            "aramDamageTaken",
                            "aramDamageDealt",
                            "aramHealing",
                            "aramShielding",
                            "urfDamageTaken",
                            "urfDamageDealt",
                            "urfHealing",
                            "urfShielding")

        champion_id = champion['id']

        login_token = login_in_mongo_api()
        url = f"http://127.0.0.1:5999/champions/{champion_id}"
        request_put = put_method_to_api(url=url, token=login_token, dictionary=champion)

        if request_put.status_code in (200, 201):
            print("Requisição bem sucedida\n", "code: ", request_put.status_code)
            counter_inserted_champions += 1
        else:
            counter_not_inserted_champions += 1

            print("--------------------------------\nErro na requisição PUT",
                  "\nitem_id: ", champion_id,
                  "\nmessage: ", request_put.status_code,
                  "\ncontent: ", request_put.content, end="\n\n")

    print(f"Total Champions = {total_champions}")
    print(f"Inserted {counter_inserted_champions} champions in database.")
    print(f"{counter_not_inserted_champions} Champions with problem.")


update_champions_in_bd()
