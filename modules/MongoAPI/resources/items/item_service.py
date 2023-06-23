from modules.MongoAPI.resources.service_utils import get_dict_content_from_endpoints, pop_items_from_dict, login_in_mongo_api, put_method_to_api


def update_items_in_bd():
    """
    This method update collections 'items' in database with meraki endpoint 'items.json'
    It uses two endpoint from MongoAPI:
        POST /login: to generate a token
        PUT /items/{item_id}: to insert/update items in DB
    Returns:
        Nothing
    """
    from modules.MongoAPI.resources.service_config import items_meraki_endpoint

    data = get_dict_content_from_endpoints(items_meraki_endpoint)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid value of data. Data need to be a dict, but it is a {type(data)}.")

    total_items = 0
    counter_inserted_items = 0
    counter_not_inserted_items = 0
    for item in data.values():
        total_items += 1

        # this method pop unnecessary items from 'item'
        # pop_items_from_dict accept numerous params to pop
        # DROP FROM MERAKI: iconOverlay, icon
        pop_items_from_dict(item, "IconOverlay", "icon")

        if item.get('no_effects') is False or item.get('no_effects'):
            item['noEffects'] = item.pop('no_effects')

        item_id = item['id']

        login_token = login_in_mongo_api()
        url = f"http://127.0.0.1:5999/items/{item_id}"
        request_put = put_method_to_api(url=url, token=login_token, dictionary=item)

        if request_put.status_code in (200, 201):
            print('Requisição bem sucedida!')

            counter_inserted_items += 1
        else:
            counter_not_inserted_items += 1

            print("--------------------------------\nErro na requisição PUT",
                  "\nitem_id: ", item_id,
                  "\nmessage: ", request_put.status_code,
                  "\ncontent: ", request_put.content, end="\n\n")

    print(f"Total items = {total_items}")
    print(f"Inserted {counter_inserted_items} items in database.")
    print(f"{counter_not_inserted_items} Items with problem.")


update_items_in_bd()
