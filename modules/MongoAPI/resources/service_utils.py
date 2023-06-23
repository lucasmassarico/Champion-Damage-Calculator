import requests
import json


def get_dict_content_from_endpoints(url):
    """
    Utils for services to get dict from content response in a HTTP GET REQUEST.
    Transform a content in a dict by json loads
    Example: item_service and champion_service usage.
    Args:
        url: string(link)

    Returns:
        data_dict: dict
    """
    response = requests.get(url)
    data = response.content
    data_dict = json.loads(data)

    return data_dict


def pop_items_from_dict(dictionary, *removed_items):
    """
    Remove items from a dict. You can pass numerous items to remove.
    Example: item_service dict
    Args:
        dictionary: dict
        *removed_items: undefined

    Returns:
        Nothing
    """
    for removed_item in removed_items:
        if dictionary.get(removed_item):
            dictionary.pop(removed_item)


def login_in_mongo_api():
    """
    Realize login in MongoAPI and get the token of login.
    Returns:
        token: string
    """
    from modules.MongoAPI.resources.service_config import db_user, db_pass, url_to_login

    login_json = {
        'username': db_user,
        'password': db_pass
    }
    login_headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url_to_login, data=json.dumps(login_json), headers=login_headers)

    return json.loads(response.content).get('access_token')


def put_method_to_api(url, token, dictionary):
    """
    Method to put json to a Database.
    Examples:
        url: http://127.0.0.1:5999/champions/266
    Args:
        url: string
        token: string
        dictionary: dict

    Returns:
        response: type requests
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {token}'
    }
    return requests.put(url, data=json.dumps(dictionary), headers=headers)
