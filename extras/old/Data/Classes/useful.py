import json
from urllib.request import urlopen
import requests


from slpp import slpp as lua

urls = {
    "champion_data": "https://leagueoflegends.fandom.com/api.php?action=query&format=json&prop=revisions&titles=Module%3AChampionData%2Fdata&rvprop=content",
    "item_data": "https://leagueoflegends.fandom.com/api.php?action=query&format=json&prop=revisions&titles=Module%3AItemData%2Fdata&rvprop=content",
    "url_base": "https://leagueoflegends.fandom.com/wiki/"
}


class Url:
    """
    Class for creating League of Legends Wiki page URLs for specific champions.

    Attributes:
        _base_url (str): Base URL of the League of Legends Wiki page.
        _champion (str): Name of the champion for which the URL should be created.

    Methods:
        __str__(): Returns the full URL for the champion's page.
    """

    def __init__(self, champion, base_url):
        self._base_url = base_url
        self._champion = champion

    def __str__(self):
        return f"{self._base_url}{self._champion.replace(' ', '_')}/LoL"


class WikiPageRetriever:
    """
    A class to retrieve data from a Wiki page and convert the data
    from a Lua pattern table to a Python dictionary.
    it is based on the api and "Module" pattern from the League of Legends Fandom page.

    Attributes:
        _url (str): The URL of the Wiki page to retrieve data from
        _retrieve_dict (dict): The converted dictionary containing the Wiki page data.

    Methods:
        _request_page(): Sends a request to the Wiki page and returns the JSON data.
        _get_page_id(data): Extracts and returns the page ID from the JSON data.
        _get_lua_unformated(data, page_id): Extracts and returns the unformatted Lua string.
        _trim_lua_string(lua_unformated): Trims the Lua string to only include the pattern table.
        _get_lua_pattern_table(): Retrieves the trimmed Lua pattern table from the Wiki page.
        _convert_lua_dict(): Converts the Lua pattern table to a Python dictionary.
    """

    def __init__(self, url):
        self._url = url
        self._retrieve_dict = self._convert_lua_dict()

    def _request_page(self):
        try:
            # faz o request na página e transforma o conteúdo em um dict
            json_url = urlopen(self._url)
            return json.loads(json_url.read().decode("utf-8"))
        except Exception as e:
            raise Exception(f'Erro ao recuperar página: {str(e)}')

    @staticmethod
    def _get_page_id(data):
        return list(data["query"]["pages"].keys())[0]

    @staticmethod
    def _get_lua_unformated(data, page_id):
        return data["query"]["pages"][page_id]["revisions"][0]["*"]

    @staticmethod
    def _trim_lua_string(lua_unformated):
        start = lua_unformated.find("{")
        end = lua_unformated.rfind("}") + 1
        return lua_unformated[start:end]

    def _get_lua_pattern_table(self):
        data = self._request_page()

        if data:
            page_id = self._get_page_id(data)
            lua_unformated = self._get_lua_unformated(data, page_id)
            return self._trim_lua_string(lua_unformated)

        return None

    def _convert_lua_dict(self):
        dict_string = self._get_lua_pattern_table()

        if dict_string:
            # converte a ‘string’ para um dicionário
            return lua.decode(dict_string)
        return None

    def return_dict(self):
        return self._retrieve_dict
